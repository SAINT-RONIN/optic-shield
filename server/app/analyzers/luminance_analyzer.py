"""Average luminance tracking and transition detection per frame."""

from __future__ import annotations

import logging

import cv2
import numpy as np

from app.models.analysis_models import LuminanceMetric, LuminanceTransitionMetric

logger = logging.getLogger(__name__)

_LUMINANCE_SCALE: float = 255.0


class LuminanceAnalyzer:
    """Measures average luminance of individual frames."""

    def analyze(self, frame: np.ndarray, timestamp: float) -> LuminanceMetric:
        """Compute the average luminance of a single frame."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        avg_lum = float(np.mean(gray)) / _LUMINANCE_SCALE
        return LuminanceMetric(
            timestamp=timestamp,
            value=avg_lum,
            avg_luminance=avg_lum,
        )

    def analyze_transition(
        self,
        frame_a: np.ndarray,
        frame_b: np.ndarray,
        timestamp: float,
    ) -> LuminanceTransitionMetric:
        """Compute luminance delta between two consecutive frames."""
        gray_a = cv2.cvtColor(frame_a, cv2.COLOR_BGR2GRAY)
        gray_b = cv2.cvtColor(frame_b, cv2.COLOR_BGR2GRAY)
        lum_a = float(np.mean(gray_a)) / _LUMINANCE_SCALE
        lum_b = float(np.mean(gray_b)) / _LUMINANCE_SCALE
        delta = abs(lum_a - lum_b)
        return LuminanceTransitionMetric(
            timestamp=timestamp,
            value=delta,
            delta=delta,
        )
