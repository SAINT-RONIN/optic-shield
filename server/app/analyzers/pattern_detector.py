"""FFT-based spatial frequency pattern detection in video frames."""

from __future__ import annotations

import logging

import cv2
import numpy as np

from app.models.analysis_models import PatternMetric, PatternRegion

logger = logging.getLogger(__name__)

_BLOCK_SIZE: int = 64
_STRIDE: int = 32
_HIGH_FREQ_THRESHOLD: float = 0.3


class PatternDetector:
    """Detects hazardous repetitive spatial patterns using 2D FFT."""

    def analyze(self, frame: np.ndarray, timestamp: float) -> PatternMetric:
        """Scan the frame for high-energy spatial frequency patterns."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape[:2]

        scores: list[float] = []
        regions: list[PatternRegion] = []

        for y in range(0, h - _BLOCK_SIZE + 1, _STRIDE):
            for x in range(0, w - _BLOCK_SIZE + 1, _STRIDE):
                block = gray[y:y + _BLOCK_SIZE, x:x + _BLOCK_SIZE]
                score = self._fft_score(block)
                scores.append(score)
                if score > _HIGH_FREQ_THRESHOLD:
                    regions.append(PatternRegion(
                        x=x, y=y, width=_BLOCK_SIZE, height=_BLOCK_SIZE,
                    ))

        avg_score = float(np.mean(scores)) if scores else 0.0

        return PatternMetric(
            timestamp=timestamp,
            value=avg_score,
            pattern_score=avg_score,
            flagged_regions=regions,
        )

    def _fft_score(self, block: np.ndarray) -> float:
        """Compute a normalized high-frequency energy score for a block."""
        f_transform = np.fft.fft2(block.astype(np.float32))
        f_shift = np.fft.fftshift(f_transform)
        magnitude = np.abs(f_shift)

        h, w = block.shape
        cy, cx = h // 2, w // 2
        radius = min(cy, cx) // 4
        magnitude[cy - radius:cy + radius, cx - radius:cx + radius] = 0

        total_energy = float(np.sum(magnitude))
        max_possible = float(h * w * 255)
        return total_energy / max_possible if max_possible > 0 else 0.0
