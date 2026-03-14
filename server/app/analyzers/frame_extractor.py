"""FFmpeg-based video frame extraction and metadata probing."""

from __future__ import annotations

import json
import logging
import os
import subprocess

from app.exceptions import AnalysisError
from app.models.analysis_models import VideoMetadata

logger = logging.getLogger(__name__)

_FFPROBE_CMD = "ffprobe"
_FFMPEG_CMD = "ffmpeg"


class FrameExtractor:
    """Extracts individual frames from a video file using FFmpeg."""

    def extract_frames(
        self, video_path: str, output_dir: str, fps: int
    ) -> list[str]:
        """Extract frames at the given FPS and return sorted file paths."""
        os.makedirs(output_dir, exist_ok=True)
        pattern = os.path.join(output_dir, "frame_%06d.jpg")
        cmd = [
            _FFMPEG_CMD, "-i", video_path,
            "-vf", f"fps={fps}",
            "-q:v", "2",
            "-y", pattern,
        ]
        try:
            subprocess.run(cmd, capture_output=True, check=True, timeout=300)
        except subprocess.CalledProcessError as exc:
            logger.error("FFmpeg failed: %s", exc.stderr[:500] if exc.stderr else "")
            raise AnalysisError("Frame extraction failed") from exc
        except FileNotFoundError as exc:
            raise AnalysisError("FFmpeg not found on system PATH") from exc

        frames = sorted(
            os.path.join(output_dir, f)
            for f in os.listdir(output_dir)
            if f.endswith(".jpg")
        )
        logger.info("Extracted %d frames from %s", len(frames), video_path)
        return frames

    def probe_metadata(self, video_path: str) -> VideoMetadata:
        """Use ffprobe to extract video metadata."""
        cmd = [
            _FFPROBE_CMD,
            "-v", "quiet",
            "-print_format", "json",
            "-show_format", "-show_streams",
            "-select_streams", "v:0",
            video_path,
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, check=True, timeout=30)
        except subprocess.CalledProcessError as exc:
            logger.error("ffprobe failed: %s", exc.stderr[:500] if exc.stderr else "")
            raise AnalysisError("Video metadata extraction failed") from exc
        except FileNotFoundError as exc:
            raise AnalysisError("ffprobe not found on system PATH") from exc

        data = json.loads(result.stdout)
        stream = data.get("streams", [{}])[0]
        fmt = data.get("format", {})

        fps_parts = stream.get("r_frame_rate", "30/1").split("/")
        fps_val = float(fps_parts[0]) / float(fps_parts[1]) if len(fps_parts) == 2 else 30.0

        return VideoMetadata(
            filename=os.path.basename(video_path),
            duration=float(fmt.get("duration", 0)),
            fps=fps_val,
            width=int(stream.get("width", 0)),
            height=int(stream.get("height", 0)),
            file_size_bytes=int(fmt.get("size", 0)),
        )
