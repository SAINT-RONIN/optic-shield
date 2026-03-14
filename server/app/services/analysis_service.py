import logging

from app.config import Settings
from app.models.analysis_models import AnalysisResult, VideoMetadata

logger = logging.getLogger(__name__)


class AnalysisService:
    """Orchestrates the full video analysis pipeline."""

    def __init__(self, config: Settings) -> None:
        self._config = config

    async def analyze_video(
        self, video_id: str, file_path: str
    ) -> AnalysisResult:
        """Run the analysis pipeline on an uploaded video file."""
        logger.info("Analysing video_id=%s at %s", video_id, file_path)
        placeholder_metadata = VideoMetadata(
            filename="",
            duration=0.0,
            fps=0.0,
            width=0,
            height=0,
            file_size_bytes=0,
        )
        return AnalysisResult(
            video_id=video_id,
            video_metadata=placeholder_metadata,
            safety_score=100.0,
            verdict="Analysis pending",
        )

    async def get_analysis(self, video_id: str) -> AnalysisResult | None:
        """Retrieve a previously completed analysis result by video ID."""
        logger.info("Fetching analysis for video_id=%s", video_id)
        return None
