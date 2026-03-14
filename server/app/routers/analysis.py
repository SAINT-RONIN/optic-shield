import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi import status as http_status

from app.config import Settings, settings
from app.models.analysis_models import AnalysisResult, ApiResponse
from app.services.analysis_service import AnalysisService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analyze", tags=["analysis"])


def _get_analysis_service() -> AnalysisService:
    return AnalysisService(config=settings)


@router.post(
    "/",
    response_model=ApiResponse[dict],
    status_code=http_status.HTTP_202_ACCEPTED,
)
async def upload_video(
    file: UploadFile,
    service: Annotated[AnalysisService, Depends(_get_analysis_service)],
) -> ApiResponse[dict]:
    """Accept a video file upload and queue it for analysis."""
    if not file.filename:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="No file provided",
        )
    logger.info("Received upload: %s", file.filename)
    return ApiResponse(
        success=True,
        data={"message": "Upload received", "filename": file.filename},
    )


@router.get(
    "/{video_id}",
    response_model=ApiResponse[AnalysisResult],
)
async def get_analysis(
    video_id: str,
    service: Annotated[AnalysisService, Depends(_get_analysis_service)],
) -> ApiResponse[AnalysisResult]:
    """Retrieve the analysis result for a previously uploaded video."""
    result = await service.get_analysis(video_id)
    if result is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"No analysis found for video_id '{video_id}'",
        )
    return ApiResponse(success=True, data=result)
