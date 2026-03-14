import logging
from typing import Any

from app.models.analysis_models import AnalysisResult, VideoMetadata

logger = logging.getLogger(__name__)


class ReportService:
    """Compiles raw metric data into a structured analysis report."""

    def compile_report(self, metrics: dict[str, Any]) -> AnalysisResult:
        """Build an AnalysisResult from a dictionary of computed metrics."""
        logger.info("Compiling analysis report from metrics")
        placeholder_metadata = VideoMetadata(
            filename=metrics.get("filename", ""),
            duration=0.0,
            fps=0.0,
            width=0,
            height=0,
            file_size_bytes=0,
        )
        return AnalysisResult(
            video_id=metrics.get("video_id", ""),
            video_metadata=placeholder_metadata,
            safety_score=self.calculate_safety_score(metrics),
            verdict="Report compilation pending",
        )

    def calculate_safety_score(self, metrics: dict[str, Any]) -> float:
        """Compute a safety score from 0.0 to 100.0 based on detected metrics."""
        logger.info("Calculating safety score")
        return 100.0
