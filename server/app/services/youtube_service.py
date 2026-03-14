"""YouTube video download and metadata extraction via yt-dlp."""

from __future__ import annotations

import logging
import os
import re
import uuid

import yt_dlp

from app.config import Settings
from app.exceptions import YouTubeError, VideoValidationError
from app.models.youtube_models import YouTubeDownloadResult, YouTubeVideoInfo

logger = logging.getLogger(__name__)

_YOUTUBE_URL_PATTERN = re.compile(
    r"^(https?://)?(www\.)?"
    r"(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/|youtube\.com/embed/)"
    r"[\w\-]{11}"
)

_MAX_DURATION_SECONDS: int = 300
_MAX_FILE_SIZE_BYTES: int = 100_000_000
_DOWNLOAD_TIMEOUT: int = 30


class YouTubeService:
    """Handles YouTube video download and metadata retrieval."""

    def __init__(self, config: Settings) -> None:
        self._config = config

    def validate_url(self, url: str) -> bool:
        """Return True if URL matches a recognized YouTube pattern."""
        return bool(_YOUTUBE_URL_PATTERN.match(url))

    async def download(self, url: str) -> YouTubeDownloadResult:
        """Download a YouTube video and return metadata + file path."""
        if not self.validate_url(url):
            raise VideoValidationError("Invalid YouTube URL")

        info = self._extract_info(url)
        self._validate_video_info(info)

        video_id = str(uuid.uuid4())
        file_path = self._download_video(url, video_id)

        metadata = YouTubeVideoInfo(
            title=info.get("title", "Unknown"),
            duration=float(info.get("duration", 0)),
            resolution=f"{info.get('width', 0)}x{info.get('height', 0)}",
            thumbnail=info.get("thumbnail"),
            channel=info.get("channel") or info.get("uploader"),
        )

        return YouTubeDownloadResult(
            video_id=video_id,
            file_path=file_path,
            metadata=metadata,
        )

    def _extract_info(self, url: str) -> dict:
        """Extract video info without downloading."""
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "socket_timeout": _DOWNLOAD_TIMEOUT,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info is None:
                    raise YouTubeError("Could not extract video info")
                return info
        except yt_dlp.utils.DownloadError as exc:
            raise YouTubeError(f"YouTube error: {exc}") from exc

    def _validate_video_info(self, info: dict) -> None:
        """Check duration and availability."""
        duration = info.get("duration", 0)
        if duration and duration > _MAX_DURATION_SECONDS:
            raise VideoValidationError(
                f"Video duration {duration}s exceeds {_MAX_DURATION_SECONDS}s limit"
            )
        if info.get("is_live"):
            raise VideoValidationError("Live streams are not supported")

    def _download_video(self, url: str, video_id: str) -> str:
        """Download the video file to temp directory."""
        output_dir = os.path.join(self._config.temp_dir, video_id)
        os.makedirs(output_dir, exist_ok=True)
        output_template = os.path.join(output_dir, "%(id)s.%(ext)s")

        ydl_opts = {
            "format": "mp4[height<=720]/best[height<=720]/best",
            "outtmpl": output_template,
            "max_filesize": _MAX_FILE_SIZE_BYTES,
            "socket_timeout": _DOWNLOAD_TIMEOUT,
            "quiet": True,
            "no_warnings": True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except yt_dlp.utils.DownloadError as exc:
            raise YouTubeError(f"Download failed: {exc}") from exc

        for f in os.listdir(output_dir):
            if f.endswith((".mp4", ".webm", ".mkv")):
                return os.path.join(output_dir, f)

        raise YouTubeError("Downloaded file not found")
