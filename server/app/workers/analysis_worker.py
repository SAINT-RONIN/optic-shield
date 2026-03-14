"""Worker function for parallel frame analysis across process pool."""

from __future__ import annotations

import logging

import cv2
import numpy as np

logger = logging.getLogger(__name__)


def analyze_frame_chunk(
    frame_paths: list[str],
    start_index: int,
    extraction_fps: int,
    video_fps: float,
) -> dict[str, list[dict]]:
    """Analyze a chunk of frames through all detectors.

    Returns a dict of metric lists serialized as dicts (for pickle transport).
    Must import analyzers inside the function for multiprocessing compatibility.
    """
    from app.analyzers.color_cycle_detector import ColorCycleDetector
    from app.analyzers.flash_detector import FlashDetector
    from app.analyzers.luminance_analyzer import LuminanceAnalyzer
    from app.analyzers.motion_analyzer import MotionAnalyzer
    from app.analyzers.pattern_detector import PatternDetector
    from app.analyzers.red_flash_detector import RedFlashDetector
    from app.analyzers.scene_cut_detector import SceneCutDetector

    flash_det = FlashDetector()
    red_flash_det = RedFlashDetector()
    lum_analyzer = LuminanceAnalyzer()
    motion_det = MotionAnalyzer()
    scene_det = SceneCutDetector()
    color_det = ColorCycleDetector()
    pattern_det = PatternDetector()

    results: dict[str, list[dict]] = {
        "flash": [], "red_flash": [], "luminance": [],
        "luminance_trans": [], "motion": [], "scene_cuts": [],
        "color_cycle": [], "pattern": [],
    }

    prev_frame: np.ndarray | None = None
    for i, path in enumerate(frame_paths):
        frame = cv2.imread(path)
        if frame is None:
            continue
        global_idx = start_index + i
        ts = float(global_idx) / extraction_fps

        results["luminance"].append(lum_analyzer.analyze(frame, ts).model_dump())
        results["pattern"].append(pattern_det.analyze(frame, ts).model_dump())

        if prev_frame is not None:
            results["flash"].append(
                flash_det.analyze(prev_frame, frame, ts, video_fps).model_dump()
            )
            results["red_flash"].append(
                red_flash_det.analyze(prev_frame, frame, ts).model_dump()
            )
            results["luminance_trans"].append(
                lum_analyzer.analyze_transition(prev_frame, frame, ts).model_dump()
            )
            results["motion"].append(
                motion_det.analyze(prev_frame, frame, ts).model_dump()
            )
            results["scene_cuts"].append(
                scene_det.analyze(prev_frame, frame, ts).model_dump()
            )
            results["color_cycle"].append(
                color_det.analyze(prev_frame, frame, ts, video_fps).model_dump()
            )

        prev_frame = frame

    logger.info(
        "Chunk starting at %d processed %d frames",
        start_index, len(frame_paths),
    )
    return results
