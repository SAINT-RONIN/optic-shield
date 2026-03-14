"""Histogram-based scene cut detection between consecutive frames."""

from __future__ import annotations

import logging

import cv2
import numpy as np

from app.models.analysis_models import SceneCutMetric

logger = logging.getLogger(__name__)

_HIST_BINS: int = 64
_HIST_RANGE: tuple[float, float] = (0.0, 256.0)


class SceneCutDetector:
    """Detects hard scene cuts using histogram comparison."""

    def analyze(
        self,
        frame_a: np.ndarray,
        frame_b: np.ndarray,
        timestamp: float,
    ) -> SceneCutMetric:
        """Estimate scene cut probability using chi-squared histogram distance."""
        hist_a = self._compute_histogram(frame_a)
        hist_b = self._compute_histogram(frame_b)

        chi_sq = cv2.compareHist(hist_a, hist_b, cv2.HISTCMP_CHISQR)
        confidence = min(1.0, chi_sq / 1000.0)

        return SceneCutMetric(
            timestamp=timestamp,
            value=confidence,
            cut_confidence=confidence,
        )

    def _compute_histogram(self, frame: np.ndarray) -> np.ndarray:
        """Compute a normalized color histogram for the frame."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist(
            [hsv], [0, 1], None,
            [_HIST_BINS, _HIST_BINS],
            [_HIST_RANGE[0], _HIST_RANGE[1], _HIST_RANGE[0], _HIST_RANGE[1]],
        )
        cv2.normalize(hist, hist)
        return hist
