"""Router for serving video files for the frontend player."""

from __future__ import annotations

import logging
import os

from fastapi import APIRouter, HTTPException
from fastapi import status as http_status
from fastapi.responses import FileResponse

from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/video", tags=["video"])


@router.get("/{video_id}")
async def serve_video(video_id: str) -> FileResponse:
    """Serve an uploaded video file for the frontend player."""
    video_dir = os.path.join(settings.temp_dir, video_id)
    if not os.path.isdir(video_dir):
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"No video found for video_id '{video_id}'",
        )
    video_files = [
        f for f in os.listdir(video_dir)
        if f.endswith((".mp4", ".webm", ".mov")) and not f.startswith(".")
    ]
    if not video_files:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Video file not found",
        )
    file_path = os.path.join(video_dir, video_files[0])
    return FileResponse(file_path, media_type="video/mp4")
