from __future__ import annotations

from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class TimestampedMetric(BaseModel):
    """Base metric tied to a specific point in video time."""

    timestamp: float = Field(description="Position in the video in seconds")
    value: float = Field(description="Generic scalar value for the metric")


class FlashMetric(TimestampedMetric):
    """Measures general flash frequency between two consecutive frames."""

    flash_count_per_second: float = Field(
        description="Number of flash transitions detected per second at this timestamp"
    )


class RedFlashMetric(TimestampedMetric):
    """Measures saturated-red flash intensity between two consecutive frames."""

    red_flash_intensity: float = Field(
        description="Intensity of red flash transition in the range [0.0, 1.0]"
    )


class LuminanceMetric(TimestampedMetric):
    """Measures average luminance of a single frame."""

    avg_luminance: float = Field(
        description="Mean relative luminance of the frame in the range [0.0, 1.0]"
    )


class LuminanceTransitionMetric(TimestampedMetric):
    """Measures the absolute luminance change between two consecutive frames."""

    delta: float = Field(
        description="Absolute difference in average luminance between frames"
    )


class MotionMetric(TimestampedMetric):
    """Measures overall motion intensity between two consecutive frames."""

    motion_intensity: float = Field(
        description="Normalised motion magnitude in the range [0.0, 1.0]"
    )


class SceneCutMetric(TimestampedMetric):
    """Measures confidence that a hard scene cut occurred between two frames."""

    cut_confidence: float = Field(
        description="Probability that a scene cut occurred, in the range [0.0, 1.0]"
    )


class ColorCycleMetric(TimestampedMetric):
    """Measures how rapidly the dominant hue is shifting between frames."""

    hue_shift_speed: float = Field(
        description="Rate of hue change in degrees per second"
    )


class PatternRegion(BaseModel):
    """Bounding box of a spatial region flagged for hazardous repetitive patterns."""

    x: int = Field(description="Left edge of the region in pixels")
    y: int = Field(description="Top edge of the region in pixels")
    width: int = Field(description="Width of the region in pixels")
    height: int = Field(description="Height of the region in pixels")


class PatternMetric(TimestampedMetric):
    """Measures the presence of seizure-risk spatial patterns within a frame."""

    pattern_score: float = Field(
        description="Aggregate hazard score for spatial patterns in the range [0.0, 1.0]"
    )
    flagged_regions: list[PatternRegion] = Field(
        default_factory=list,
        description="Bounding boxes of regions containing hazardous patterns",
    )


class DangerZone(BaseModel):
    """A contiguous time range in the video identified as potentially hazardous."""

    start_time: float = Field(description="Start of the danger zone in seconds")
    end_time: float = Field(description="End of the danger zone in seconds")
    severity: Literal["low", "medium", "high", "critical"] = Field(
        description="Severity level of the detected hazard"
    )
    reason: str = Field(description="Human-readable explanation of the hazard")


class VideoMetadata(BaseModel):
    """Technical metadata extracted from the source video file."""

    filename: str = Field(description="Original filename of the uploaded video")
    duration: float = Field(description="Total duration of the video in seconds")
    fps: float = Field(description="Frame rate of the video in frames per second")
    width: int = Field(description="Horizontal resolution in pixels")
    height: int = Field(description="Vertical resolution in pixels")
    file_size_bytes: int = Field(description="Size of the video file in bytes")


class AnalysisRequest(BaseModel):
    """Request payload for triggering a video analysis job."""

    video_id: str = Field(description="Unique identifier for the uploaded video")
    api_key: str | None = Field(
        default=None,
        description="Anthropic API key for AI report generation (BYOK)",
    )


class AnalysisResult(BaseModel):
    """Complete analysis output for a single video."""

    video_id: str = Field(description="Unique identifier for the analysed video")
    video_metadata: VideoMetadata = Field(description="Technical metadata of the video")
    safety_score: float = Field(
        description="Overall safety score from 0.0 (most dangerous) to 100.0 (safe)"
    )
    verdict: str = Field(description="Short human-readable safety verdict")
    flash_metrics: list[FlashMetric] = Field(default_factory=list)
    red_flash_metrics: list[RedFlashMetric] = Field(default_factory=list)
    luminance_metrics: list[LuminanceMetric] = Field(default_factory=list)
    luminance_transitions: list[LuminanceTransitionMetric] = Field(default_factory=list)
    motion_metrics: list[MotionMetric] = Field(default_factory=list)
    scene_cut_metrics: list[SceneCutMetric] = Field(default_factory=list)
    color_cycle_metrics: list[ColorCycleMetric] = Field(default_factory=list)
    pattern_metrics: list[PatternMetric] = Field(default_factory=list)
    danger_zones: list[DangerZone] = Field(default_factory=list)
    ai_report: str | None = Field(
        default=None,
        description="AI-generated narrative report (requires API key)",
    )
    graph_explanations: dict[str, str] = Field(
        default_factory=dict,
        description="Per-graph AI explanations keyed by metric name",
    )


class AnalysisProgress(BaseModel):
    """Real-time progress update broadcast over WebSocket during analysis."""

    video_id: str = Field(description="Identifier of the video being analysed")
    stage: str = Field(description="Name of the current processing stage")
    progress: float = Field(
        description="Completion fraction of the current stage in the range [0.0, 1.0]"
    )
    current_frame: int = Field(default=0, description="Index of the frame being processed")
    total_frames: int = Field(default=0, description="Total number of frames to process")
    message: str = Field(default="", description="Optional human-readable status message")


class ApiResponse(BaseModel, Generic[T]):
    """Standard envelope wrapping every REST API response."""

    success: bool = Field(description="Whether the request completed without error")
    data: T | None = Field(default=None, description="Response payload on success")
    error: str | None = Field(default=None, description="Error message on failure")
    error_code: str | None = Field(
        default=None, description="Machine-readable error code on failure"
    )
