import logging

logger = logging.getLogger(__name__)


class FrameExtractor:
    """Extracts individual frames from a video file at a specified frame rate."""

    def __init__(self) -> None:
        pass

    def extract_frames(
        self, video_path: str, output_dir: str, fps: int
    ) -> list[str]:
        """Extract frames from a video and write them to output_dir.

        Returns a list of absolute paths to the extracted frame images.
        """
        logger.info(
            "Extracting frames from %s at %d fps into %s",
            video_path,
            fps,
            output_dir,
        )
        return []
