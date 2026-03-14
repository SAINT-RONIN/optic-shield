import logging

from fastapi import APIRouter, HTTPException
from fastapi import status as http_status
from fastapi.responses import FileResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/video", tags=["video"])


@router.get("/{video_id}")
async def stream_video(video_id: str) -> FileResponse:
    """Serve a previously uploaded video file by its identifier."""
    logger.info("Video stream requested for video_id=%s", video_id)
    raise HTTPException(
        status_code=http_status.HTTP_404_NOT_FOUND,
        detail=f"Video '{video_id}' not found",
    )
