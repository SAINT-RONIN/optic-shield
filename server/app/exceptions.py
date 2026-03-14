from enum import Enum
from typing import Any


class ErrorCode(str, Enum):
    """Enumeration of all domain-level error codes used in API error responses."""

    VIDEO_VALIDATION_ERROR = "VIDEO_VALIDATION_ERROR"
    ANALYSIS_ERROR = "ANALYSIS_ERROR"
    YOUTUBE_ERROR = "YOUTUBE_ERROR"
    AI_SERVICE_ERROR = "AI_SERVICE_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class OpticShieldError(Exception):
    """Base exception for all domain errors raised within Optic Shield AI."""

    error_code: ErrorCode = ErrorCode.INTERNAL_ERROR

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        error_code: ErrorCode | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.details = details
        if error_code is not None:
            self.error_code = error_code


class VideoValidationError(OpticShieldError):
    """Raised when an uploaded video fails format, size, or duration validation."""

    error_code: ErrorCode = ErrorCode.VIDEO_VALIDATION_ERROR


class AnalysisError(OpticShieldError):
    """Raised when the frame analysis pipeline encounters an unrecoverable error."""

    error_code: ErrorCode = ErrorCode.ANALYSIS_ERROR


class YouTubeError(OpticShieldError):
    """Raised when a YouTube download or metadata fetch operation fails."""

    error_code: ErrorCode = ErrorCode.YOUTUBE_ERROR


class AIServiceError(OpticShieldError):
    """Raised when the Anthropic API call fails or returns an unexpected response."""

    error_code: ErrorCode = ErrorCode.AI_SERVICE_ERROR
