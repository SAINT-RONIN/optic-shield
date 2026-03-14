"""Saturated-red flash transition detection between consecutive frames."""

from __future__ import annotations

import logging

import cv2
import numpy as np

from app.models.analysis_models import RedFlashMetric

logger = logging.getLogger(__name__)

_RED_DOMINANCE_THRESHOLD: float = 0.8
_RED_MARGIN_THRESHOLD: float = 0.4
_INTENSITY_SCALE: float = 255.0


class RedFlashDetector:
    """Detects saturated-red flash transitions between frames."""

    def analyze(
        self,
        frame_a: np.ndarray,
        frame_b: np.ndarray,
        timestamp: float,
    ) -> RedFlashMetric:
        """Measure red flash intensity between two consecutive frames."""
        red_a = self._red_saturation_score(frame_a)
        red_b = self._red_saturation_score(frame_b)
        intensity = abs(red_a - red_b)

        return RedFlashMetric(
            timestamp=timestamp,
            value=intensity,
            red_flash_intensity=intensity,
        )

    def _red_saturation_score(self, frame: np.ndarray) -> float:
        """Compute a 0-1 score for how red-saturated the frame is."""
        b, g, r = (
            frame[:, :, 0].astype(np.float32) / _INTENSITY_SCALE,
            frame[:, :, 1].astype(np.float32) / _INTENSITY_SCALE,
            frame[:, :, 2].astype(np.float32) / _INTENSITY_SCALE,
        )
        max_gb = np.maximum(g, b)
        mask = (r > _RED_DOMINANCE_THRESHOLD) & ((r - max_gb) > _RED_MARGIN_THRESHOLD)
        return float(np.mean(mask))
