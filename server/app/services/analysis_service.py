"""Orchestrates the full video analysis pipeline."""

from __future__ import annotations

import logging
import os
import shutil
from typing import Callable

import cv2
import numpy as np

from app.analyzers.flash_detector import FlashDetector
from app.analyzers.frame_extractor import FrameExtractor
from app.analyzers.luminance_analyzer import LuminanceAnalyzer
from app.config import Settings
from app.exceptions import AnalysisError
from app.models.analysis_models import (
    AnalysisProgress,
    AnalysisResult,
    DangerZone,
    FlashMetric,
    LuminanceMetric,
    LuminanceTransitionMetric,
    VideoMetadata,
)
from app.utils.thresholds import (
    MAX_GENERAL_FLASHES_PER_SECOND,
    SAFE_SCORE_THRESHOLD,
)

logger = logging.getLogger(__name__)

ProgressCallback = Callable[[AnalysisProgress], None]

_FLASH_PENALTY: float = 5.0
_LUMINANCE_PENALTY: float = 3.0
_DANGER_ZONE_GAP_SECONDS: float = 1.0


class AnalysisService:
    """Orchestrates video analysis: extraction, detection, scoring."""

    _results: dict[str, AnalysisResult] = {}

    def __init__(self, config: Settings) -> None:
        self._config = config
        self._extractor = FrameExtractor()
        self._flash_detector = FlashDetector()
        self._luminance_analyzer = LuminanceAnalyzer()

    async def analyze_video(
        self,
        video_id: str,
        file_path: str,
        progress_cb: ProgressCallback | None = None,
    ) -> AnalysisResult:
        """Run the full analysis pipeline on an uploaded video."""
        logger.info("Starting analysis for video_id=%s", video_id)

        def report(stage: str, progress: float, frame: int = 0, total: int = 0) -> None:
            if progress_cb:
                progress_cb(AnalysisProgress(
                    video_id=video_id, stage=stage, progress=progress,
                    current_frame=frame, total_frames=total,
                ))

        metadata = self._extractor.probe_metadata(file_path)
        report("Extracting frames", 0.0)

        frames_dir = os.path.join(self._config.temp_dir, video_id, "frames")
        frame_paths = self._extractor.extract_frames(
            file_path, frames_dir, self._config.extraction_fps
        )
        if not frame_paths:
            raise AnalysisError("No frames extracted from video")

        total = len(frame_paths)
        report("Extracting frames", 1.0, total, total)

        flash_metrics, lum_metrics, lum_transitions = self._run_detectors(
            frame_paths, metadata.fps, video_id, total, report
        )

        report("Generating report", 0.8)
        score = self._compute_score(flash_metrics, lum_transitions)
        danger_zones = self._find_danger_zones(flash_metrics, metadata.fps)
        verdict = self._score_to_verdict(score)

        result = AnalysisResult(
            video_id=video_id,
            video_metadata=metadata,
            safety_score=score,
            verdict=verdict,
            flash_metrics=flash_metrics,
            luminance_metrics=lum_metrics,
            luminance_transitions=lum_transitions,
            danger_zones=danger_zones,
        )
        AnalysisService._results[video_id] = result

        self._cleanup_frames(frames_dir)
        report("Complete", 1.0, total, total)
        logger.info("Analysis complete for video_id=%s score=%.1f", video_id, score)
        return result

    def _run_detectors(
        self,
        frame_paths: list[str],
        fps: float,
        video_id: str,
        total: int,
        report: Callable[..., None],
    ) -> tuple[list[FlashMetric], list[LuminanceMetric], list[LuminanceTransitionMetric]]:
        """Run flash and luminance detectors on all frame pairs."""
        flash_metrics: list[FlashMetric] = []
        lum_metrics: list[LuminanceMetric] = []
        lum_transitions: list[LuminanceTransitionMetric] = []
        extraction_fps = self._config.extraction_fps

        prev_frame: np.ndarray | None = None
        for i, path in enumerate(frame_paths):
            frame = cv2.imread(path)
            if frame is None:
                continue
            timestamp = float(i) / extraction_fps

            lum_metrics.append(self._luminance_analyzer.analyze(frame, timestamp))

            if prev_frame is not None:
                flash_metrics.append(
                    self._flash_detector.analyze(prev_frame, frame, timestamp, fps)
                )
                lum_transitions.append(
                    self._luminance_analyzer.analyze_transition(prev_frame, frame, timestamp)
                )
            prev_frame = frame

            if i % 50 == 0:
                report("Analyzing frames", float(i) / total, i, total)

        return flash_metrics, lum_metrics, lum_transitions

    def _compute_score(
        self,
        flash_metrics: list[FlashMetric],
        lum_transitions: list[LuminanceTransitionMetric],
    ) -> float:
        """Compute safety score: 100 minus penalties for violations."""
        score = 100.0
        for m in flash_metrics:
            if m.flash_count_per_second > MAX_GENERAL_FLASHES_PER_SECOND:
                score -= _FLASH_PENALTY
        for m in lum_transitions:
            if m.delta > 0.2:
                score -= _LUMINANCE_PENALTY
        return max(0.0, min(100.0, score))

    def _find_danger_zones(
        self, flash_metrics: list[FlashMetric], fps: float
    ) -> list[DangerZone]:
        """Identify contiguous time ranges with flash violations."""
        violations = [m for m in flash_metrics if m.flash_count_per_second > MAX_GENERAL_FLASHES_PER_SECOND]
        if not violations:
            return []
        zones: list[DangerZone] = []
        start = violations[0].timestamp
        end = start
        for m in violations[1:]:
            if m.timestamp - end <= _DANGER_ZONE_GAP_SECONDS:
                end = m.timestamp
            else:
                zones.append(DangerZone(start_time=start, end_time=end, severity="high", reason="Flash rate exceeds 3/sec"))
                start = m.timestamp
                end = start
        zones.append(DangerZone(start_time=start, end_time=end, severity="high", reason="Flash rate exceeds 3/sec"))
        return zones

    def _score_to_verdict(self, score: float) -> str:
        """Convert numeric score to human-readable verdict."""
        if score >= SAFE_SCORE_THRESHOLD:
            return "Safe — no significant issues detected"
        if score >= 50.0:
            return "Caution — review flagged segments"
        return "Unsafe — immediate fixes recommended"

    def _cleanup_frames(self, frames_dir: str) -> None:
        """Remove extracted frame images."""
        try:
            shutil.rmtree(frames_dir, ignore_errors=True)
        except OSError:
            logger.warning("Failed to clean up frames dir: %s", frames_dir)

    async def get_analysis(self, video_id: str) -> AnalysisResult | None:
        """Retrieve a previously completed analysis result."""
        return AnalysisService._results.get(video_id)
