"""Orchestrates the full video analysis pipeline with parallel processing."""

from __future__ import annotations

import logging
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Callable

from app.analyzers.frame_extractor import FrameExtractor
from app.config import Settings
from app.exceptions import AnalysisError, VideoValidationError
from app.models.analysis_models import (
    AnalysisProgress, AnalysisResult,
    ColorCycleMetric, FlashMetric, LuminanceMetric,
    LuminanceTransitionMetric, MotionMetric, PatternMetric,
    RedFlashMetric, SceneCutMetric,
)
from app.services.report_service import ReportService
from app.utils.cleanup import cleanup_video_files

logger = logging.getLogger(__name__)

ProgressCallback = Callable[[AnalysisProgress], None]

_MIN_FRAMES_FOR_PARALLEL: int = 200
_MAX_WORKERS: int = 4


class AnalysisService:
    """Orchestrates video analysis with parallel frame processing."""

    _results: dict[str, AnalysisResult] = {}

    def __init__(self, config: Settings) -> None:
        self._config = config
        self._extractor = FrameExtractor()
        self._report = ReportService()

    async def analyze_video(
        self, video_id: str, file_path: str,
        progress_cb: ProgressCallback | None = None,
    ) -> AnalysisResult:
        """Run the full analysis pipeline on an uploaded video."""
        logger.info("Starting analysis for video_id=%s", video_id)

        def report(stage: str, pct: float, frame: int = 0, total: int = 0) -> None:
            if progress_cb:
                progress_cb(AnalysisProgress(
                    video_id=video_id, stage=stage, progress=pct,
                    current_frame=frame, total_frames=total,
                ))

        metadata = self._extractor.probe_metadata(file_path)
        self._validate_duration(metadata.duration)
        report("Extracting frames", 0.0)

        frames_dir = os.path.join(self._config.temp_dir, video_id, "frames")
        frame_paths = self._extractor.extract_frames(
            file_path, frames_dir, self._config.extraction_fps,
        )
        if not frame_paths:
            raise AnalysisError("No frames extracted from video")

        total = len(frame_paths)
        report("Extracting frames", 1.0, total, total)
        report("Analyzing frames", 0.0, 0, total)

        metrics = self._run_parallel(frame_paths, metadata.fps, total, report)
        report("Generating report", 0.9)

        score = self._report.calculate_safety_score(
            metrics["flash"], metrics["red_flash"], metrics["luminance_trans"],
            metrics["motion"], metrics["scene_cuts"],
            metrics["color_cycle"], metrics["pattern"],
        )
        zones = self._report.find_danger_zones(
            metrics["flash"], metrics["red_flash"],
            metrics["motion"], metrics["pattern"],
        )

        result = AnalysisResult(
            video_id=video_id, video_metadata=metadata,
            safety_score=score, verdict=self._report.score_to_verdict(score),
            flash_metrics=metrics["flash"],
            red_flash_metrics=metrics["red_flash"],
            luminance_metrics=metrics["luminance"],
            luminance_transitions=metrics["luminance_trans"],
            motion_metrics=metrics["motion"],
            scene_cut_metrics=metrics["scene_cuts"],
            color_cycle_metrics=metrics["color_cycle"],
            pattern_metrics=metrics["pattern"],
            danger_zones=zones,
        )
        AnalysisService._results[video_id] = result
        cleanup_video_files(video_id, self._config.temp_dir, keep_video=True)
        report("Complete", 1.0, total, total)
        logger.info("Analysis complete video_id=%s score=%.1f", video_id, score)
        return result

    def _validate_duration(self, duration: float) -> None:
        """Raise if video exceeds the configured max duration."""
        max_dur = self._config.max_video_duration_seconds
        if duration > max_dur:
            raise VideoValidationError(
                f"Video duration {duration:.0f}s exceeds {max_dur}s limit"
            )

    def _run_parallel(
        self, frame_paths: list[str], fps: float, total: int,
        report: Callable[..., None],
    ) -> dict[str, list]:
        """Split frames into chunks and process in parallel."""
        from app.workers.analysis_worker import analyze_frame_chunk

        n_workers = min(_MAX_WORKERS, max(1, (os.cpu_count() or 2) - 1))
        chunk_size = max(1, total // n_workers)
        chunks: list[tuple[list[str], int]] = []
        for i in range(0, total, chunk_size):
            chunks.append((frame_paths[i:i + chunk_size], i))

        if total < _MIN_FRAMES_FOR_PARALLEL or n_workers <= 1:
            raw = analyze_frame_chunk(
                frame_paths, 0, self._config.extraction_fps, fps,
            )
            report("Analyzing frames", 1.0, total, total)
            return self._deserialize_metrics(raw)

        all_raw: list[dict[str, list[dict]]] = []
        with ProcessPoolExecutor(max_workers=n_workers) as pool:
            futures = {
                pool.submit(
                    analyze_frame_chunk, paths, start,
                    self._config.extraction_fps, fps,
                ): start
                for paths, start in chunks
            }
            done_count = 0
            for future in as_completed(futures):
                all_raw.append(future.result())
                done_count += 1
                report("Analyzing frames", done_count / len(chunks), 0, total)

        return self._merge_and_deserialize(all_raw)

    def _deserialize_metrics(self, raw: dict[str, list[dict]]) -> dict[str, list]:
        """Convert dicts back to Pydantic model instances."""
        return {
            "flash": [FlashMetric(**d) for d in raw["flash"]],
            "red_flash": [RedFlashMetric(**d) for d in raw["red_flash"]],
            "luminance": [LuminanceMetric(**d) for d in raw["luminance"]],
            "luminance_trans": [LuminanceTransitionMetric(**d) for d in raw["luminance_trans"]],
            "motion": [MotionMetric(**d) for d in raw["motion"]],
            "scene_cuts": [SceneCutMetric(**d) for d in raw["scene_cuts"]],
            "color_cycle": [ColorCycleMetric(**d) for d in raw["color_cycle"]],
            "pattern": [PatternMetric(**d) for d in raw["pattern"]],
        }

    def _merge_and_deserialize(
        self, chunks: list[dict[str, list[dict]]],
    ) -> dict[str, list]:
        """Merge multiple chunk results and deserialize."""
        merged: dict[str, list[dict]] = {
            "flash": [], "red_flash": [], "luminance": [],
            "luminance_trans": [], "motion": [], "scene_cuts": [],
            "color_cycle": [], "pattern": [],
        }
        for chunk in chunks:
            for key in merged:
                merged[key].extend(chunk[key])
        for key in merged:
            merged[key].sort(key=lambda d: d.get("timestamp", 0))
        return self._deserialize_metrics(merged)

    async def get_analysis(self, video_id: str) -> AnalysisResult | None:
        """Retrieve a previously completed analysis result."""
        return AnalysisService._results.get(video_id)
