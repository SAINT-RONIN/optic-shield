"""Prompt builders that serialize AnalysisResult data for LLM consumption."""

from __future__ import annotations

from app.models.analysis_models import AnalysisResult
from app.prompts.analysis_serializers import (
    _fmt_size,
    _fmt_time,
    _serialize_color_cycle_metrics,
    _serialize_danger_zones,
    _serialize_flash_metrics,
    _serialize_luminance_metrics,
    _serialize_motion_metrics,
    _serialize_pattern_metrics,
    _serialize_red_flash_metrics,
    _serialize_scene_cut_metrics,
)


def serialize_analysis_context(result: AnalysisResult) -> str:
    """Convert an AnalysisResult into a concise LLM-ready text summary."""
    meta = result.video_metadata
    duration = _fmt_time(meta.duration)

    sections: list[str] = [
        "=== VIDEO SAFETY ANALYSIS CONTEXT ===\n",
        f"File: {meta.filename}",
        f"Duration: {duration} ({meta.duration:.1f}s)",
        f"Resolution: {meta.width}x{meta.height} @ {meta.fps:.2f} fps",
        f"Size: {_fmt_size(meta.file_size_bytes)}\n",
        f"Safety Score: {result.safety_score:.1f}/100",
        f"Verdict: {result.verdict}\n",
        "--- DANGER ZONES ---",
        _serialize_danger_zones(result),
        "--- FLASH METRICS ---",
        _serialize_flash_metrics(result),
        "--- RED FLASH METRICS ---",
        _serialize_red_flash_metrics(result),
        "--- LUMINANCE METRICS ---",
        _serialize_luminance_metrics(result),
        "--- MOTION METRICS ---",
        _serialize_motion_metrics(result),
        "--- SCENE CUTS ---",
        _serialize_scene_cut_metrics(result),
        "--- COLOR CYCLING ---",
        _serialize_color_cycle_metrics(result),
        "--- SPATIAL PATTERNS ---",
        _serialize_pattern_metrics(result),
        "=== END OF CONTEXT ===",
    ]
    return "\n".join(sections)


def build_report_prompt(result: AnalysisResult) -> str:
    """Build the user message asking the AI to generate a comprehensive safety report."""
    context = serialize_analysis_context(result)
    return (
        f"{context}\n\n"
        "Based on the analysis data above, generate a comprehensive video safety report. "
        "Structure your report with these sections:\n\n"
        "1. OVERALL ASSESSMENT — Safety score interpretation and verdict explanation.\n"
        "2. DANGER ZONES — Detail every danger zone: timestamp range, severity, medical risk, "
        "and why it is dangerous.\n"
        "3. VIOLATIONS BY METRIC — For each metric with violations, list the specific "
        "timestamps, peak values with units, and WCAG threshold exceeded.\n"
        "4. SEVERITY RATINGS — Rate each violation on the clinical scale: "
        "critical (immediate seizure risk), high (likely trigger), "
        "medium (risk for highly sensitive viewers), low (borderline).\n"
        "5. RECOMMENDED FIXES — Provide specific remediation steps. Include FFmpeg commands "
        "where applicable with exact filter parameters.\n"
        "6. COMPLIANCE STATUS — State clearly whether the video passes or fails "
        "WCAG 2.1 SC 2.3.1 (Level A) and SC 2.3.2 (Level AAA).\n\n"
        "Be specific with timestamps in m:ss format. Do not omit any danger zone."
    )


def build_graph_explanation_prompt(
    metric_name: str,
    metrics_summary: str,
    threshold_info: str,
) -> str:
    """Build a prompt requesting a 2-3 sentence graph explanation."""
    return (
        f"You are analyzing the {metric_name} graph from a video safety analysis.\n\n"
        f"Graph data summary:\n{metrics_summary}\n\n"
        f"Relevant threshold: {threshold_info}\n\n"
        "Write exactly 2-3 sentences explaining what this graph shows, whether any "
        "thresholds are exceeded, and what that means for viewer safety. "
        "Be specific with values and units. Do not use bullet points."
    )
