"""Pure colour-space conversion utilities with no side effects."""


def rgb_to_luminance(r: float, g: float, b: float) -> float:
    """Compute relative luminance from linear RGB using ITU-R BT.709 coefficients.

    Inputs are expected in the range [0.0, 1.0].
    Returns relative luminance in the range [0.0, 1.0].
    """
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def rgb_to_hsl(r: float, g: float, b: float) -> tuple[float, float, float]:
    """Convert RGB to HSL colour space.

    Inputs are expected in the range [0.0, 1.0].
    Returns (hue [0, 360), saturation [0, 1], lightness [0, 1]).
    """
    c_max = max(r, g, b)
    c_min = min(r, g, b)
    delta = c_max - c_min
    lightness = (c_max + c_min) / 2.0

    if delta == 0.0:
        return 0.0, 0.0, lightness

    saturation = delta / (1.0 - abs(2.0 * lightness - 1.0))

    if c_max == r:
        hue = 60.0 * (((g - b) / delta) % 6)
    elif c_max == g:
        hue = 60.0 * (((b - r) / delta) + 2)
    else:
        hue = 60.0 * (((r - g) / delta) + 4)

    return hue % 360.0, saturation, lightness


def is_saturated_red(r: float, g: float, b: float) -> bool:
    """Return True if the colour qualifies as a saturated red per WCAG criteria.

    A colour is saturated red when the red component exceeds both green and blue
    by a significant margin, following the W3C definition used in flash analysis.
    Inputs are expected in the range [0.0, 1.0].
    """
    return r > 0.8 and r - max(g, b) > 0.4
