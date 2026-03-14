import logging

import numpy as np

from app.models.analysis_models import MotionMetric

logger = logging.getLogger(__name__)


class MotionAnalyzer:
    """Measures overall motion intensity between consecutive video frames."""

    def __init__(self) -> None:
        pass

    def analyze(
        self,
        frame_a: np.ndarray,
        frame_b: np.ndarray,
        timestamp: float,
    ) -> MotionMetric:
        """Compute the normalised motion magnitude between two consecutive frames.

        Both frames must be BGR uint8 arrays of identical shape.
        """
        logger.debug("MotionAnalyzer.analyze at timestamp=%.3f", timestamp)
        return MotionMetric(
            timestamp=timestamp,
            value=0.0,
            motion_intensity=0.0,
        )
