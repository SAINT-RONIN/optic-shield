import logging

import numpy as np

from app.models.analysis_models import SceneCutMetric

logger = logging.getLogger(__name__)


class SceneCutDetector:
    """Detects hard scene cuts between consecutive video frames."""

    def __init__(self) -> None:
        pass

    def analyze(
        self,
        frame_a: np.ndarray,
        frame_b: np.ndarray,
        timestamp: float,
    ) -> SceneCutMetric:
        """Estimate the probability that a scene cut occurred between two frames.

        Both frames must be BGR uint8 arrays of identical shape.
        """
        logger.debug("SceneCutDetector.analyze at timestamp=%.3f", timestamp)
        return SceneCutMetric(
            timestamp=timestamp,
            value=0.0,
            cut_confidence=0.0,
        )
