"""Pure utility functions for cleaning up temporary files."""
import logging
import os

logger = logging.getLogger(__name__)


def cleanup_temp_files(directory: str, max_age_seconds: int) -> int:
    """Delete files in directory that are older than max_age_seconds.

    Returns the number of files deleted. Returns 0 until implemented.
    """
    logger.info(
        "cleanup_temp_files called: directory=%s, max_age=%ds",
        directory,
        max_age_seconds,
    )
    return 0


def cleanup_video_files(video_id: str, temp_dir: str) -> None:
    """Remove all temporary files associated with video_id from temp_dir."""
    logger.info(
        "cleanup_video_files called: video_id=%s, temp_dir=%s",
        video_id,
        temp_dir,
    )
