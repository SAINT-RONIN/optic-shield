# W3C / WCAG 2.1 SC 2.3.1 flash and spatial pattern thresholds.
# All values are sourced from the Photosensitive Epilepsy Analysis Tool (PEAT)
# guidelines and the W3C Working Group Note on Three Flashes or Below Threshold.

# Maximum number of general (luminance) flashes permitted per second.
MAX_GENERAL_FLASHES_PER_SECOND: int = 3

# Minimum luminance change (cd/m²) that constitutes a flash transition.
FLASH_LUMINANCE_CHANGE_THRESHOLD: float = 20.0

# Minimum relative luminance delta (0–1 scale) that constitutes a flash.
FLASH_RELATIVE_LUMINANCE_THRESHOLD: float = 0.1

# Fraction of the total screen area that a flash must cover to be reportable.
FLASH_AREA_THRESHOLD: float = 0.25

# Minimum number of high-contrast spatial cycles per degree of visual field
# that triggers the spatial pattern hazard.
SPATIAL_PATTERN_CYCLES_THRESHOLD: int = 8

# Maximum number of saturated-red flash transitions permitted per second.
MAX_RED_FLASH_TRANSITIONS: int = 5

# Safety score at or above which the video is considered safe.
SAFE_SCORE_THRESHOLD: float = 80.0

# Safety score below which the video is considered a warning-level hazard.
WARNING_SCORE_THRESHOLD: float = 50.0

# Safety score below which the video is considered a critical-level hazard.
CRITICAL_SCORE_THRESHOLD: float = 20.0
