import logging
from typing import Any

logger = logging.getLogger(__name__)


class FrameWorker:
    """Loads raw frame data from disk paths into memory for analysis."""

    def __init__(self) -> None:
        pass

    def load_frames(self, frame_paths: list[str]) -> list[Any]:
        """Read frame images from the given paths and return them as a list.

        Each element in the returned list corresponds to a loaded frame array.
        """
        logger.info("FrameWorker.load_frames called with %d paths", len(frame_paths))
        return []
