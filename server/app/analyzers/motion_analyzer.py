"""Motion intensity measurement between consecutive video frames."""

from __future__ import annotations

import logging

import cv2
import numpy as np

from app.models.analysis_models import MotionMetric

logger = logging.getLogger(__name__)

_MOTION_SCALE: float = 255.0


class MotionAnalyzer:
    """Measures overall motion intensity via absolute pixel differences."""

    def analyze(
        self,
        frame_a: np.ndarray,
        frame_b: np.ndarray,
        timestamp: float,
    ) -> MotionMetric:
        """Compute normalized motion intensity between two frames."""
        gray_a = cv2.cvtColor(frame_a, cv2.COLOR_BGR2GRAY)
        gray_b = cv2.cvtColor(frame_b, cv2.COLOR_BGR2GRAY)

        diff = cv2.absdiff(gray_a, gray_b)
        intensity = float(np.mean(diff)) / _MOTION_SCALE

        return MotionMetric(
            timestamp=timestamp,
            value=intensity,
            motion_intensity=intensity,
        )
