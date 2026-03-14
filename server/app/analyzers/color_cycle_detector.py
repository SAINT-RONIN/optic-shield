"""Dominant hue tracking to detect rapid color cycling between frames."""

from __future__ import annotations

import logging

import cv2
import numpy as np

from app.models.analysis_models import ColorCycleMetric

logger = logging.getLogger(__name__)

_HUE_SCALE: float = 2.0  # OpenCV hue range is 0-179, convert to 0-358


class ColorCycleDetector:
    """Detects rapid hue cycling between consecutive frames."""

    def analyze(
        self,
        frame_a: np.ndarray,
        frame_b: np.ndarray,
        timestamp: float,
        fps: float = 10.0,
    ) -> ColorCycleMetric:
        """Measure hue shift speed between two consecutive frames."""
        hue_a = self._dominant_hue(frame_a)
        hue_b = self._dominant_hue(frame_b)

        raw_diff = abs(hue_a - hue_b)
        hue_diff = min(raw_diff, 360.0 - raw_diff)
        shift_speed = hue_diff * fps

        return ColorCycleMetric(
            timestamp=timestamp,
            value=shift_speed,
            hue_shift_speed=shift_speed,
        )

    def _dominant_hue(self, frame: np.ndarray) -> float:
        """Find the dominant hue in the frame using histogram peak."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hue_channel = hsv[:, :, 0]
        hist = cv2.calcHist([hue_channel], [0], None, [180], [0, 180])
        dominant_bin = int(np.argmax(hist))
        return float(dominant_bin) * _HUE_SCALE
