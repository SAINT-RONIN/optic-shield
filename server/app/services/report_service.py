"""Compiles metric data into scored analysis reports with danger zone identification."""

from __future__ import annotations

import logging

from app.models.analysis_models import (
    AnalysisResult,
    ColorCycleMetric,
    DangerZone,
    FlashMetric,
    LuminanceTransitionMetric,
    MotionMetric,
    PatternMetric,
    RedFlashMetric,
    SceneCutMetric,
)
from app.utils.thresholds import (
    MAX_GENERAL_FLASHES_PER_SECOND,
    MAX_RED_FLASH_TRANSITIONS,
    SAFE_SCORE_THRESHOLD,
    WARNING_SCORE_THRESHOLD,
)

logger = logging.getLogger(__name__)

_FLASH_WEIGHT: float = 5.0
_RED_FLASH_WEIGHT: float = 4.0
_LUMINANCE_WEIGHT: float = 3.0
_MOTION_WEIGHT: float = 1.5
_SCENE_CUT_WEIGHT: float = 1.0
_COLOR_CYCLE_WEIGHT: float = 2.0
_PATTERN_WEIGHT: float = 3.0

_DANGER_GAP_SECONDS: float = 1.0
_RED_INTENSITY_THRESHOLD: float = 0.2
_LUMINANCE_DELTA_THRESHOLD: float = 0.2
_MOTION_THRESHOLD: float = 0.7
_CUT_CONFIDENCE_THRESHOLD: float = 0.8
_HUE_SPEED_THRESHOLD: float = 180.0
_PATTERN_SCORE_THRESHOLD: float = 0.5


class ReportService:
    """Compiles raw metric data into scored analysis results."""

    def calculate_safety_score(
        self,
        flash: list[FlashMetric],
        red_flash: list[RedFlashMetric],
        luminance_trans: list[LuminanceTransitionMetric],
        motion: list[MotionMetric],
        scene_cuts: list[SceneCutMetric],
        color_cycle: list[ColorCycleMetric],
        pattern: list[PatternMetric],
    ) -> float:
        """Compute safety score 0-100 by subtracting weighted penalties."""
        score = 100.0
        score -= sum(_FLASH_WEIGHT for m in flash if m.flash_count_per_second > MAX_GENERAL_FLASHES_PER_SECOND)
        score -= sum(_RED_FLASH_WEIGHT for m in red_flash if m.red_flash_intensity > _RED_INTENSITY_THRESHOLD)
        score -= sum(_LUMINANCE_WEIGHT for m in luminance_trans if m.delta > _LUMINANCE_DELTA_THRESHOLD)
        score -= sum(_MOTION_WEIGHT for m in motion if m.motion_intensity > _MOTION_THRESHOLD)
        score -= sum(_SCENE_CUT_WEIGHT for m in scene_cuts if m.cut_confidence > _CUT_CONFIDENCE_THRESHOLD)
        score -= sum(_COLOR_CYCLE_WEIGHT for m in color_cycle if m.hue_shift_speed > _HUE_SPEED_THRESHOLD)
        score -= sum(_PATTERN_WEIGHT for m in pattern if m.pattern_score > _PATTERN_SCORE_THRESHOLD)
        return max(0.0, min(100.0, score))

    def find_danger_zones(
        self,
        flash: list[FlashMetric],
        red_flash: list[RedFlashMetric],
        motion: list[MotionMetric],
        pattern: list[PatternMetric],
    ) -> list[DangerZone]:
        """Identify contiguous time ranges with violations."""
        violations: list[tuple[float, str]] = []
        for m in flash:
            if m.flash_count_per_second > MAX_GENERAL_FLASHES_PER_SECOND:
                violations.append((m.timestamp, "Flash rate exceeds 3/sec"))
        for m in red_flash:
            if m.red_flash_intensity > _RED_INTENSITY_THRESHOLD:
                violations.append((m.timestamp, "Red flash intensity high"))
        for m in motion:
            if m.motion_intensity > _MOTION_THRESHOLD:
                violations.append((m.timestamp, "High motion intensity"))
        for m in pattern:
            if m.pattern_score > _PATTERN_SCORE_THRESHOLD:
                violations.append((m.timestamp, "Hazardous spatial pattern"))

        violations.sort(key=lambda v: v[0])
        return self._merge_zones(violations)

    def _merge_zones(self, violations: list[tuple[float, str]]) -> list[DangerZone]:
        """Merge nearby violations into contiguous danger zones."""
        if not violations:
            return []
        zones: list[DangerZone] = []
        start, reason = violations[0]
        end = start
        reasons: set[str] = {reason}
        for ts, r in violations[1:]:
            if ts - end <= _DANGER_GAP_SECONDS:
                end = ts
                reasons.add(r)
            else:
                severity = "critical" if len(reasons) > 2 else "high" if len(reasons) > 1 else "medium"
                zones.append(DangerZone(
                    start_time=start, end_time=end,
                    severity=severity, reason="; ".join(sorted(reasons)),
                ))
                start, end = ts, ts
                reasons = {r}
        severity = "critical" if len(reasons) > 2 else "high" if len(reasons) > 1 else "medium"
        zones.append(DangerZone(
            start_time=start, end_time=end,
            severity=severity, reason="; ".join(sorted(reasons)),
        ))
        return zones

    def score_to_verdict(self, score: float) -> str:
        """Convert score to human-readable verdict."""
        if score >= SAFE_SCORE_THRESHOLD:
            return "Safe — no significant issues detected"
        if score >= WARNING_SCORE_THRESHOLD:
            return "Caution — review flagged segments"
        return "Unsafe — immediate fixes recommended"
