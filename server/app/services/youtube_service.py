import logging
import re

from app.config import Settings
from app.models.youtube_models import YouTubeDownloadResult

logger = logging.getLogger(__name__)

_YOUTUBE_URL_PATTERN = re.compile(
    r"^(https?://)?(www\.)?"
    r"(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)"
    r"[\w\-]{11}"
)


class YouTubeService:
    """Handles YouTube video download and metadata retrieval."""

    def __init__(self, config: Settings) -> None:
        self._config = config

    async def download(self, url: str) -> YouTubeDownloadResult:
        """Download a YouTube video to the configured temp directory."""
        logger.info("Downloading YouTube video: %s", url)
        raise NotImplementedError("YouTube download not yet implemented")

    def validate_url(self, url: str) -> bool:
        """Return True if the URL matches a recognised YouTube video URL pattern."""
        return bool(_YOUTUBE_URL_PATTERN.match(url))
