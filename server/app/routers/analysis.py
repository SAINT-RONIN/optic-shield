"""Router for video upload and analysis result retrieval."""

from __future__ import annotations

import asyncio
import logging
import os
import uuid

from fastapi import APIRouter, BackgroundTasks, HTTPException, UploadFile
from fastapi import status as http_status

from app.config import settings
from app.exceptions import AnalysisError, VideoValidationError
from app.models.analysis_models import AnalysisProgress, AnalysisResult, ApiResponse
from app.services.analysis_service import AnalysisService
from app.services.ws_manager import ws_manager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analyze", tags=["analysis"])

_ALLOWED_TYPES = {"video/mp4", "video/webm", "video/quicktime"}

_analysis_service = AnalysisService(config=settings)


def _validate_upload(file: UploadFile) -> None:
    """Validate uploaded file type and presence."""
    if not file.filename:
        raise VideoValidationError("No file provided")
    content_type = file.content_type or ""
    if content_type not in _ALLOWED_TYPES:
        raise VideoValidationError(f"Unsupported file type: {content_type}")


async def _save_upload(file: UploadFile, video_id: str) -> str:
    """Save uploaded file to temp directory and return the file path."""
    video_dir = os.path.join(settings.temp_dir, video_id)
    os.makedirs(video_dir, exist_ok=True)
    file_path = os.path.join(video_dir, file.filename or "video.mp4")
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    return file_path


async def _run_analysis(video_id: str, file_path: str) -> None:
    """Background task that runs the analysis pipeline."""
    try:
        def sync_progress(p: AnalysisProgress) -> None:
            asyncio.get_event_loop().create_task(
                ws_manager.send_progress(video_id, p.model_dump())
            )

        await _analysis_service.analyze_video(video_id, file_path, sync_progress)
    except AnalysisError:
        logger.exception("Analysis failed for video_id=%s", video_id)


@router.post(
    "/",
    response_model=ApiResponse[dict],
    status_code=http_status.HTTP_202_ACCEPTED,
)
async def upload_video(
    file: UploadFile,
    background_tasks: BackgroundTasks,
) -> ApiResponse[dict]:
    """Accept a video upload, save it, and start analysis in the background."""
    _validate_upload(file)

    video_id = str(uuid.uuid4())
    file_path = await _save_upload(file, video_id)
    logger.info("Saved upload video_id=%s path=%s", video_id, file_path)

    background_tasks.add_task(_run_analysis, video_id, file_path)

    return ApiResponse(
        success=True,
        data={"video_id": video_id, "filename": file.filename},
    )


@router.get("/{video_id}", response_model=ApiResponse[AnalysisResult])
async def get_analysis(video_id: str) -> ApiResponse[AnalysisResult]:
    """Retrieve analysis result for a previously uploaded video."""
    result = await _analysis_service.get_analysis(video_id)
    if result is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"No analysis found for video_id '{video_id}'",
        )
    return ApiResponse(success=True, data=result)
