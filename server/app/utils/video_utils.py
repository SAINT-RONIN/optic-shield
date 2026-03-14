"""Pure utility functions for extracting metadata from video files."""
import logging
from typing import Any

logger = logging.getLogger(__name__)


def get_video_metadata(file_path: str) -> dict[str, Any]:
    """Return a dictionary of technical metadata for the video at file_path.

    Returns an empty dict until the OpenCV/FFprobe implementation is added.
    """
    logger.info("get_video_metadata called for %s", file_path)
    return {}


def get_video_duration(file_path: str) -> float:
    """Return the duration of the video at file_path in seconds.

    Returns 0.0 until the OpenCV/FFprobe implementation is added.
    """
    logger.info("get_video_duration called for %s", file_path)
    return 0.0
