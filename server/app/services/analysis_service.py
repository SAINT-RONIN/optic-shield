"""Orchestrates the full video analysis pipeline."""

from __future__ import annotations

import logging
import os
import shutil
from typing import Callable

import cv2
import numpy as np

from app.analyzers.color_cycle_detector import ColorCycleDetector
from app.analyzers.flash_detector import FlashDetector
from app.analyzers.frame_extractor import FrameExtractor
from app.analyzers.luminance_analyzer import LuminanceAnalyzer
from app.analyzers.motion_analyzer import MotionAnalyzer
from app.analyzers.pattern_detector import PatternDetector
from app.analyzers.red_flash_detector import RedFlashDetector
from app.analyzers.scene_cut_detector import SceneCutDetector
from app.config import Settings
from app.exceptions import AnalysisError
from app.models.analysis_models import AnalysisProgress, AnalysisResult
from app.services.report_service import ReportService

logger = logging.getLogger(__name__)

ProgressCallback = Callable[[AnalysisProgress], None]


class _MetricsBucket:
    """Collects all metric lists during frame processing."""

    def __init__(self) -> None:
        from app.models.analysis_models import (
            ColorCycleMetric, FlashMetric, LuminanceMetric,
            LuminanceTransitionMetric, MotionMetric, PatternMetric,
            RedFlashMetric, SceneCutMetric,
        )
        self.flash: list[FlashMetric] = []
        self.red_flash: list[RedFlashMetric] = []
        self.luminance: list[LuminanceMetric] = []
        self.luminance_trans: list[LuminanceTransitionMetric] = []
        self.motion: list[MotionMetric] = []
        self.scene_cuts: list[SceneCutMetric] = []
        self.color_cycle: list[ColorCycleMetric] = []
        self.pattern: list[PatternMetric] = []


class AnalysisService:
    """Orchestrates video analysis: extraction, detection, scoring."""

    _results: dict[str, AnalysisResult] = {}

    def __init__(self, config: Settings) -> None:
        self._config = config
        self._extractor = FrameExtractor()
        self._flash = FlashDetector()
        self._red_flash = RedFlashDetector()
        self._luminance = LuminanceAnalyzer()
        self._motion = MotionAnalyzer()
        self._scene_cut = SceneCutDetector()
        self._color_cycle = ColorCycleDetector()
        self._pattern = PatternDetector()
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
        report("Extracting frames", 0.0)

        frames_dir = os.path.join(self._config.temp_dir, video_id, "frames")
        frame_paths = self._extractor.extract_frames(
            file_path, frames_dir, self._config.extraction_fps,
        )
        if not frame_paths:
            raise AnalysisError("No frames extracted from video")

        total = len(frame_paths)
        report("Extracting frames", 1.0, total, total)

        bucket = self._run_all_detectors(frame_paths, metadata.fps, total, report)
        report("Generating report", 0.9)

        score = self._report.calculate_safety_score(
            bucket.flash, bucket.red_flash, bucket.luminance_trans,
            bucket.motion, bucket.scene_cuts, bucket.color_cycle, bucket.pattern,
        )
        danger_zones = self._report.find_danger_zones(
            bucket.flash, bucket.red_flash, bucket.motion, bucket.pattern,
        )

        result = AnalysisResult(
            video_id=video_id, video_metadata=metadata,
            safety_score=score, verdict=self._report.score_to_verdict(score),
            flash_metrics=bucket.flash, red_flash_metrics=bucket.red_flash,
            luminance_metrics=bucket.luminance, luminance_transitions=bucket.luminance_trans,
            motion_metrics=bucket.motion, scene_cut_metrics=bucket.scene_cuts,
            color_cycle_metrics=bucket.color_cycle, pattern_metrics=bucket.pattern,
            danger_zones=danger_zones,
        )
        AnalysisService._results[video_id] = result
        self._cleanup_frames(frames_dir)
        report("Complete", 1.0, total, total)
        logger.info("Analysis complete video_id=%s score=%.1f", video_id, score)
        return result

    def _run_all_detectors(
        self, frame_paths: list[str], fps: float, total: int,
        report: Callable[..., None],
    ) -> _MetricsBucket:
        """Run all analyzers on every frame."""
        bucket = _MetricsBucket()
        extraction_fps = self._config.extraction_fps
        prev_frame: np.ndarray | None = None

        for i, path in enumerate(frame_paths):
            frame = cv2.imread(path)
            if frame is None:
                continue
            ts = float(i) / extraction_fps

            bucket.luminance.append(self._luminance.analyze(frame, ts))
            bucket.pattern.append(self._pattern.analyze(frame, ts))

            if prev_frame is not None:
                bucket.flash.append(self._flash.analyze(prev_frame, frame, ts, fps))
                bucket.red_flash.append(self._red_flash.analyze(prev_frame, frame, ts))
                bucket.luminance_trans.append(
                    self._luminance.analyze_transition(prev_frame, frame, ts),
                )
                bucket.motion.append(self._motion.analyze(prev_frame, frame, ts))
                bucket.scene_cuts.append(self._scene_cut.analyze(prev_frame, frame, ts))
                bucket.color_cycle.append(
                    self._color_cycle.analyze(prev_frame, frame, ts, fps),
                )

            prev_frame = frame
            if i % 50 == 0:
                report("Analyzing frames", float(i) / total, i, total)

        return bucket

    def _cleanup_frames(self, frames_dir: str) -> None:
        """Remove extracted frame images."""
        try:
            shutil.rmtree(frames_dir, ignore_errors=True)
        except OSError:
            logger.warning("Failed to clean up frames dir: %s", frames_dir)

    async def get_analysis(self, video_id: str) -> AnalysisResult | None:
        """Retrieve a previously completed analysis result."""
        return AnalysisService._results.get(video_id)
