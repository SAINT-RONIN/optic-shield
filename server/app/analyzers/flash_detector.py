import logging

import numpy as np

from app.models.analysis_models import FlashMetric

logger = logging.getLogger(__name__)


class FlashDetector:
    """Detects general luminance-based flash transitions between consecutive frames."""

    def __init__(self) -> None:
        pass

    def analyze(
        self,
        frame_a: np.ndarray,
        frame_b: np.ndarray,
        timestamp: float,
    ) -> FlashMetric:
        """Compare two consecutive frames and return a flash frequency metric.

        Both frames must be BGR uint8 arrays of identical shape.
        """
        logger.debug("FlashDetector.analyze at timestamp=%.3f", timestamp)
        return FlashMetric(
            timestamp=timestamp,
            value=0.0,
            flash_count_per_second=0.0,
        )
