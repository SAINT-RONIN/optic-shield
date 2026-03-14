"""Batch frame loading for multiprocessing analysis pipeline."""

from __future__ import annotations

import logging
from typing import Any

import cv2
import numpy as np

logger = logging.getLogger(__name__)


def load_frame_batch(frame_paths: list[str]) -> list[tuple[int, np.ndarray | None]]:
    """Load a batch of frames from disk.

    Returns list of (index, frame) tuples. Frame is None if load fails.
    """
    results: list[tuple[int, np.ndarray | None]] = []
    for i, path in enumerate(frame_paths):
        frame = cv2.imread(path)
        if frame is None:
            logger.warning("Failed to load frame: %s", path)
        results.append((i, frame))
    return results
