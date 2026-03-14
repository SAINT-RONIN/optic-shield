from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application configuration loaded from environment variables or .env file."""

    temp_dir: str = Field(default="./tmp", description="Directory for temporary video files")
    max_video_duration_seconds: int = Field(
        default=300, description="Maximum allowed video duration in seconds"
    )
    max_file_size_bytes: int = Field(
        default=104857600, description="Maximum allowed upload size in bytes (100 MB)"
    )
    extraction_fps: int = Field(
        default=10, description="Frames per second to extract during analysis"
    )
    cors_origins: list[str] = Field(
        default=["http://localhost:5173"],
        description="Allowed CORS origins for the frontend",
    )

    model_config = {"env_file": ".env"}


settings = Settings()
