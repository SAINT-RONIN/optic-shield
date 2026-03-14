import logging

import numpy as np

from app.models.analysis_models import RedFlashMetric

logger = logging.getLogger(__name__)


class RedFlashDetector:
    """Detects saturated-red flash transitions between consecutive frames."""

    def __init__(self) -> None:
        pass

    def analyze(
        self,
        frame_a: np.ndarray,
        frame_b: np.ndarray,
        timestamp: float,
    ) -> RedFlashMetric:
        """Compare two consecutive frames and return a red flash intensity metric.

        Both frames must be BGR uint8 arrays of identical shape.
        """
        logger.debug("RedFlashDetector.analyze at timestamp=%.3f", timestamp)
        return RedFlashMetric(
            timestamp=timestamp,
            value=0.0,
            red_flash_intensity=0.0,
        )
