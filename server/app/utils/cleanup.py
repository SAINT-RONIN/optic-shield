"""Utility functions for cleaning up temporary files."""

from __future__ import annotations

import logging
import os
import shutil
import time

logger = logging.getLogger(__name__)


def cleanup_temp_files(directory: str, max_age_seconds: int) -> int:
    """Delete files in directory older than max_age_seconds. Returns count deleted."""
    if not os.path.isdir(directory):
        return 0
    deleted = 0
    now = time.time()
    for entry in os.listdir(directory):
        path = os.path.join(directory, entry)
        try:
            if os.path.isdir(path) and (now - os.path.getmtime(path)) > max_age_seconds:
                shutil.rmtree(path, ignore_errors=True)
                deleted += 1
        except OSError:
            logger.warning("Failed to check/delete: %s", path)
    logger.info("Cleaned up %d items from %s", deleted, directory)
    return deleted


def cleanup_video_files(
    video_id: str, temp_dir: str, keep_video: bool = False,
) -> None:
    """Remove temporary files for a video analysis. Optionally keep the video file."""
    video_dir = os.path.join(temp_dir, video_id)
    if not os.path.isdir(video_dir):
        return
    frames_dir = os.path.join(video_dir, "frames")
    if os.path.isdir(frames_dir):
        shutil.rmtree(frames_dir, ignore_errors=True)
        logger.info("Cleaned up frames for video_id=%s", video_id)
    if not keep_video:
        shutil.rmtree(video_dir, ignore_errors=True)
        logger.info("Cleaned up all files for video_id=%s", video_id)
