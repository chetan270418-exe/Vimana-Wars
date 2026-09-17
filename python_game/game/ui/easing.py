"""
game/ui/easing.py
Easing curves for smooth UI animations.
Premium-indie motion grammar — every value transition should flow through one of these.
"""
import math


# ── Linear ──────────────────────────────────────────────────────────────

def linear(t: float) -> float:
    return t


# ── Cubic ───────────────────────────────────────────────────────────────

def ease_in_cubic(t: float) -> float:
    return t * t * t


def ease_out_cubic(t: float) -> float:
    return 1.0 - (1.0 - t) ** 3


def ease_in_out_cubic(t: float) -> float:
    return 4.0 * t * t * t if t < 0.5 else 1.0 - (-2.0 * t + 2.0) ** 3 / 2.0


# ── Quart ───────────────────────────────────────────────────────────────

def ease_out_quart(t: float) -> float:
    return 1.0 - (1.0 - t) ** 4


def ease_in_out_quart(t: float) -> float:
    return 8.0 * t * t * t * t if t < 0.5 else 1.0 - (-2.0 * t + 2.0) ** 4 / 2.0


# ── Back (overshoot) ───────────────────────────────────────────────────

def ease_out_back(t: float, s: float = 1.70158) -> float:
    return 1.0 + (s + 1.0) * (t - 1.0) ** 3 + s * (t - 1.0) ** 2


def ease_in_back(t: float, s: float = 1.70158) -> float:
    return (s + 1.0) * t * t * t - s * t * t


# ── Elastic (spring) ───────────────────────────────────────────────────

def ease_out_elastic(t: float) -> float:
    if t == 0.0 or t == 1.0:
        return t
    return math.pow(2.0, -10.0 * t) * math.sin((t * 10.0 - 0.75) * 2.094) + 1.0


def ease_in_elastic(t: float) -> float:
    if t == 0.0 or t == 1.0:
        return t
    return -math.pow(2.0, 10.0 * t - 10.0) * math.sin((t * 10.0 - 10.75) * 2.094)


# ── Bounce ──────────────────────────────────────────────────────────────

def ease_out_bounce(t: float) -> float:
    if t < 1.0 / 2.75:
        return 7.5625 * t * t
    elif t < 2.0 / 2.75:
        t -= 1.5 / 2.75
        return 7.5625 * t * t + 0.75
    elif t < 2.5 / 2.75:
        t -= 2.25 / 2.75
        return 7.5625 * t * t + 0.9375
    else:
        t -= 2.625 / 2.75
        return 7.5625 * t * t + 0.984375


# ── Expo ────────────────────────────────────────────────────────────────

def ease_out_expo(t: float) -> float:
    return 1.0 if t == 1.0 else 1.0 - math.pow(2.0, -10.0 * t)


# ── Utility helpers ─────────────────────────────────────────────────────

def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation from a to b by t (0..1)."""
    return a + (b - a) * t


def lerp_color(c1: tuple, c2: tuple, t: float) -> tuple:
    """Linearly interpolate between two RGB or RGBA color tuples."""
    return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def approach(current: float, target: float, step: float) -> float:
    """Move current toward target by at most step."""
    if abs(current - target) <= step:
        return target
    return current + math.copysign(step, target - current)


def inverse_lerp(a: float, b: float, v: float) -> float:
    """Returns t such that lerp(a, b, t) == v. Returns 0 if a == b."""
    if abs(b - a) < 1e-9:
        return 0.0
    return clamp((v - a) / (b - a))


def remap(v: float, in_lo: float, in_hi: float, out_lo: float, out_hi: float) -> float:
    """Map value v from [in_lo, in_hi] to [out_lo, out_hi]."""
    t = inverse_lerp(in_lo, in_hi, v)
    return lerp(out_lo, out_hi, t)
