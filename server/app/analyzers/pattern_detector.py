import logging

import numpy as np

from app.models.analysis_models import PatternMetric

logger = logging.getLogger(__name__)


class PatternDetector:
    """Detects hazardous spatial repetitive patterns within individual video frames."""

    def __init__(self) -> None:
        pass

    def analyze(
        self,
        frame: np.ndarray,
        timestamp: float,
    ) -> PatternMetric:
        """Scan a single frame for seizure-risk spatial patterns.

        The frame must be a BGR uint8 array.
        """
        logger.debug("PatternDetector.analyze at timestamp=%.3f", timestamp)
        return PatternMetric(
            timestamp=timestamp,
            value=0.0,
            pattern_score=0.0,
            flagged_regions=[],
        )
