from __future__ import annotations

from pydantic import BaseModel, Field


class YouTubeRequest(BaseModel):
    """Request payload for downloading and analysing a YouTube video."""

    url: str = Field(description="Full YouTube video URL to download")
    api_key: str | None = Field(
        default=None, description="API key for AI report generation"
    )


class YouTubeVideoInfo(BaseModel):
    """Metadata describing a YouTube video retrieved before downloading."""

    title: str = Field(description="Title of the YouTube video")
    duration: float = Field(description="Duration of the video in seconds")
    resolution: str = Field(
        description="Video resolution string, e.g. '1920x1080'"
    )
    thumbnail: str | None = Field(
        default=None, description="URL of the video thumbnail image"
    )
    channel: str | None = Field(
        default=None, description="Name of the YouTube channel that published the video"
    )


class YouTubeDownloadResult(BaseModel):
    """Result of a successful YouTube video download."""

    video_id: str = Field(
        description="Internal unique identifier assigned to the downloaded video"
    )
    file_path: str = Field(
        description="Absolute path to the downloaded video file on disk"
    )
    metadata: YouTubeVideoInfo = Field(
        description="Metadata extracted from the YouTube video"
    )
