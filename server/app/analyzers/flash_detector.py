"""Flash frequency detection between consecutive video frames."""

from __future__ import annotations

import logging

import cv2
import numpy as np

from app.models.analysis_models import FlashMetric
from app.utils.thresholds import FLASH_RELATIVE_LUMINANCE_THRESHOLD

logger = logging.getLogger(__name__)

_LUMINANCE_SCALE: float = 255.0


class FlashDetector:
    """Detects general luminance-based flash transitions between frames."""

    def analyze(
        self,
        frame_a: np.ndarray,
        frame_b: np.ndarray,
        timestamp: float,
        fps: float = 10.0,
    ) -> FlashMetric:
        """Compare two consecutive frames and return flash frequency metric."""
        gray_a = cv2.cvtColor(frame_a, cv2.COLOR_BGR2GRAY)
        gray_b = cv2.cvtColor(frame_b, cv2.COLOR_BGR2GRAY)

        lum_a = float(np.mean(gray_a)) / _LUMINANCE_SCALE
        lum_b = float(np.mean(gray_b)) / _LUMINANCE_SCALE
        delta = abs(lum_a - lum_b)

        is_flash = delta > FLASH_RELATIVE_LUMINANCE_THRESHOLD
        flash_rate = fps if is_flash else 0.0

        return FlashMetric(
            timestamp=timestamp,
            value=delta,
            flash_count_per_second=flash_rate,
        )
