import logging

import numpy as np

from app.models.analysis_models import LuminanceMetric

logger = logging.getLogger(__name__)


class LuminanceAnalyzer:
    """Measures average perceptual luminance of individual video frames."""

    def __init__(self) -> None:
        pass

    def analyze(
        self,
        frame: np.ndarray,
        timestamp: float,
    ) -> LuminanceMetric:
        """Compute the average relative luminance of a single frame.

        The frame must be a BGR uint8 array.
        """
        logger.debug("LuminanceAnalyzer.analyze at timestamp=%.3f", timestamp)
        return LuminanceMetric(
            timestamp=timestamp,
            value=0.0,
            avg_luminance=0.0,
        )
