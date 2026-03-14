import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from app.config import settings
from app.models.analysis_models import ApiResponse
from app.models.youtube_models import YouTubeDownloadResult, YouTubeRequest
from app.services.youtube_service import YouTubeService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/youtube", tags=["youtube"])


def _get_youtube_service() -> YouTubeService:
    return YouTubeService(config=settings)


@router.post("/", response_model=ApiResponse[YouTubeDownloadResult])
async def download_youtube_video(
    body: YouTubeRequest,
    service: Annotated[YouTubeService, Depends(_get_youtube_service)],
) -> ApiResponse[YouTubeDownloadResult]:
    """Validate a YouTube URL and queue the video for download and analysis."""
    if not service.validate_url(body.url):
        return ApiResponse(
            success=False,
            error="Invalid YouTube URL",
            error_code="VIDEO_VALIDATION_ERROR",
        )
    logger.info("YouTube download requested: %s", body.url)
    return ApiResponse(
        success=False,
        error="YouTube download not yet implemented",
        error_code="INTERNAL_ERROR",
    )
