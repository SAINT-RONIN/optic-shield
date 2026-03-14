"""Private serialization helpers for converting AnalysisResult fields to LLM-ready text."""

from __future__ import annotations

from app.models.analysis_models import AnalysisResult

_MAX_VIOLATIONS_PER_METRIC: int = 10
_SECONDS_PER_MINUTE: int = 60


def _fmt_time(seconds: float) -> str:
    """Convert seconds to human-readable m:ss format."""
    minutes = int(seconds) // _SECONDS_PER_MINUTE
    secs = int(seconds) % _SECONDS_PER_MINUTE
    return f"{minutes}:{secs:02d}"


def _fmt_size(size_bytes: int) -> str:
    """Convert bytes to MB string."""
    return f"{size_bytes / 1_048_576:.1f} MB"


def _serialize_danger_zones(result: AnalysisResult) -> str:
    """Serialize all danger zones with full detail — never truncated."""
    if not result.danger_zones:
        return "  None detected.\n"

    lines: list[str] = []
    for zone in result.danger_zones:
        start = _fmt_time(zone.start_time)
        end = _fmt_time(zone.end_time)
        lines.append(
            f"  [{zone.severity.upper()}] {start} – {end}: {zone.reason}"
        )
    return "\n".join(lines) + "\n"


def _serialize_flash_metrics(result: AnalysisResult) -> str:
    """Summarize flash metrics — top violations only."""
    metrics = result.flash_metrics
    if not metrics:
        return "  No data.\n"

    values = [m.flash_count_per_second for m in metrics]
    peak = max(values)
    violations = [m for m in metrics if m.flash_count_per_second > 3.0]
    violation_count = len(violations)

    lines = [
        f"  Peak: {peak:.2f} flashes/sec",
        f"  Violations (>3/sec): {violation_count}",
    ]
    for m in violations[:_MAX_VIOLATIONS_PER_METRIC]:
        lines.append(
            f"  - {_fmt_time(m.timestamp)}: {m.flash_count_per_second:.2f} flashes/sec"
        )
    return "\n".join(lines) + "\n"


def _serialize_red_flash_metrics(result: AnalysisResult) -> str:
    """Summarize red flash metrics — top violations only."""
    metrics = result.red_flash_metrics
    if not metrics:
        return "  No data.\n"

    values = [m.red_flash_intensity for m in metrics]
    peak = max(values)
    violations = [m for m in metrics if m.red_flash_intensity > 0.2]
    violation_count = len(violations)

    lines = [
        f"  Peak intensity: {peak:.3f}",
        f"  High-intensity events (>0.2): {violation_count}",
    ]
    for m in violations[:_MAX_VIOLATIONS_PER_METRIC]:
        lines.append(
            f"  - {_fmt_time(m.timestamp)}: intensity {m.red_flash_intensity:.3f}"
        )
    return "\n".join(lines) + "\n"


def _serialize_luminance_metrics(result: AnalysisResult) -> str:
    """Summarize luminance and luminance transition metrics."""
    lum = result.luminance_metrics
    trans = result.luminance_transitions

    lines: list[str] = []
    if lum:
        avg_lum = sum(m.avg_luminance for m in lum) / len(lum)
        lines.append(f"  Avg luminance: {avg_lum:.3f}")
        lines.append(f"  Min: {min(m.avg_luminance for m in lum):.3f}")
        lines.append(f"  Max: {max(m.avg_luminance for m in lum):.3f}")

    if trans:
        violations = [m for m in trans if m.delta > 0.2]
        peak_delta = max(m.delta for m in trans)
        lines.append(f"  Peak luminance delta: {peak_delta:.3f}")
        lines.append(f"  Large transitions (delta >0.2): {len(violations)}")
        for m in violations[:_MAX_VIOLATIONS_PER_METRIC]:
            lines.append(f"  - {_fmt_time(m.timestamp)}: delta {m.delta:.3f}")

    return ("\n".join(lines) + "\n") if lines else "  No data.\n"


def _serialize_motion_metrics(result: AnalysisResult) -> str:
    """Summarize motion metrics."""
    metrics = result.motion_metrics
    if not metrics:
        return "  No data.\n"

    values = [m.motion_intensity for m in metrics]
    peak = max(values)
    high_motion = [m for m in metrics if m.motion_intensity > 0.7]

    lines = [
        f"  Peak intensity: {peak:.3f}",
        f"  High-motion events (>0.7): {len(high_motion)}",
    ]
    for m in high_motion[:_MAX_VIOLATIONS_PER_METRIC]:
        lines.append(f"  - {_fmt_time(m.timestamp)}: {m.motion_intensity:.3f}")
    return "\n".join(lines) + "\n"


def _serialize_scene_cut_metrics(result: AnalysisResult) -> str:
    """Summarize scene cut metrics — count only to conserve tokens."""
    metrics = result.scene_cut_metrics
    if not metrics:
        return "  No data.\n"

    cuts = [m for m in metrics if m.cut_confidence > 0.8]
    peak = max(m.cut_confidence for m in metrics)
    return (
        f"  Detected cuts (confidence >0.8): {len(cuts)}\n"
        f"  Peak confidence: {peak:.3f}\n"
    )


def _serialize_color_cycle_metrics(result: AnalysisResult) -> str:
    """Summarize color cycle metrics — detected status and peak."""
    metrics = result.color_cycle_metrics
    if not metrics:
        return "  Not detected.\n"

    peak = max(m.hue_shift_speed for m in metrics)
    rapid = [m for m in metrics if m.hue_shift_speed > 180.0]
    return (
        f"  Peak hue shift: {peak:.1f} deg/sec\n"
        f"  Rapid cycling events (>180 deg/sec): {len(rapid)}\n"
    )


def _serialize_pattern_metrics(result: AnalysisResult) -> str:
    """Summarize pattern metrics — detected status and peak score."""
    metrics = result.pattern_metrics
    if not metrics:
        return "  Not detected.\n"

    peak = max(m.pattern_score for m in metrics)
    flagged = [m for m in metrics if m.pattern_score > 0.5]
    return (
        f"  Peak pattern score: {peak:.3f}\n"
        f"  High-hazard frames (score >0.5): {len(flagged)}\n"
    )
