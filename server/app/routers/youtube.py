"""Router for YouTube video submission and analysis."""

from __future__ import annotations

import logging

from fastapi import APIRouter, BackgroundTasks

from app.config import settings
from app.exceptions import YouTubeError, VideoValidationError
from app.models.analysis_models import AnalysisProgress, ApiResponse
from app.models.youtube_models import YouTubeDownloadResult, YouTubeRequest
from app.services.analysis_service import AnalysisService
from app.services.ws_manager import ws_manager
from app.services.youtube_service import YouTubeService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/youtube", tags=["youtube"])

_youtube_service = YouTubeService(config=settings)
_analysis_service = AnalysisService(config=settings)


async def _run_youtube_analysis(video_id: str, file_path: str) -> None:
    """Background task: run analysis on downloaded YouTube video."""
    import asyncio

    try:
        loop = asyncio.get_event_loop()

        def sync_progress(p: AnalysisProgress) -> None:
            loop.create_task(
                ws_manager.send_progress(video_id, p.model_dump())
            )

        await _analysis_service.analyze_video(
            video_id, file_path, sync_progress
        )
    except Exception:
        logger.exception(
            "YouTube analysis failed for video_id=%s", video_id
        )


@router.post("/", response_model=ApiResponse[YouTubeDownloadResult])
async def download_youtube_video(
    body: YouTubeRequest,
    background_tasks: BackgroundTasks,
) -> ApiResponse[YouTubeDownloadResult]:
    """Download a YouTube video and start analysis."""
    if not _youtube_service.validate_url(body.url):
        return ApiResponse(
            success=False,
            error="Invalid YouTube URL",
            error_code="VIDEO_VALIDATION_ERROR",
        )

    try:
        result = await _youtube_service.download(body.url)
    except (YouTubeError, VideoValidationError) as exc:
        return ApiResponse(
            success=False,
            error=str(exc),
            error_code=exc.error_code.value,
        )

    logger.info("YouTube downloaded: video_id=%s", result.video_id)
    background_tasks.add_task(
        _run_youtube_analysis, result.video_id, result.file_path
    )

    return ApiResponse(success=True, data=result)
