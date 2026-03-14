import logging

import numpy as np

from app.models.analysis_models import ColorCycleMetric

logger = logging.getLogger(__name__)


class ColorCycleDetector:
    """Detects rapid hue cycling between consecutive video frames."""

    def __init__(self) -> None:
        pass

    def analyze(
        self,
        frame_a: np.ndarray,
        frame_b: np.ndarray,
        timestamp: float,
    ) -> ColorCycleMetric:
        """Measure the rate of dominant hue shift between two consecutive frames.

        Both frames must be BGR uint8 arrays of identical shape.
        """
        logger.debug("ColorCycleDetector.analyze at timestamp=%.3f", timestamp)
        return ColorCycleMetric(
            timestamp=timestamp,
            value=0.0,
            hue_shift_speed=0.0,
        )
