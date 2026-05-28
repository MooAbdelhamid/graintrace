"""Implements the GrainTrace v2 'good photo' rejection rules.

Hard requirements (from the team's checklist):
    - Resolution ≥ 10 MP per shot
    - Sharp focus on head — no motion blur
    - Head fully visible and centred
    - Two views per bow: side + front
    - Even, diffuse lighting; plain dark background

Reject if:
    - Blurred or out of focus
    - Head cut off at the frame edge
    - Resolution below 10 MP
    - Heavy glare covers the wood grain
    - ID information missing for the session  (handled in the enrolment form,
      not per-photo)

The first four are enforced here. The fifth lives in the enrolment page since
it's a session-level fact, not a per-image one.
"""
from __future__ import annotations

import io
from dataclasses import dataclass
from typing import Literal

import numpy as np
from PIL import Image

# Thresholds
MIN_MP = 10.0              # hard reject below this
RECOMMENDED_MP = 12.0
BLUR_FAIL = 80.0           # variance-of-Laplacian below = blurry
BLUR_WARN = 200.0
ASPECT_WARN = 2.0          # max(w,h)/min(w,h) above this = head likely off-centre
ASPECT_FAIL = 3.0          # above this = banner crop, head cut off
GLARE_WARN = 0.03          # 3% saturated pixels = borderline
GLARE_FAIL = 0.10          # 10% saturated pixels = heavy glare

Status = Literal["pass", "warn", "fail"]


@dataclass
class CheckResult:
    label: str
    status: Status
    detail: str


@dataclass
class PreflightReport:
    overall: Status
    checks: list[CheckResult]


# ---------------------------------------------------------------------------
# Individual checks (each one mirrors a line in the rejection spec)
# ---------------------------------------------------------------------------


def _laplacian_variance(gray: np.ndarray) -> float:
    """Variance-of-Laplacian — a classic cheap focus / blur estimate."""
    from numpy.lib.stride_tricks import sliding_window_view
    if gray.shape[0] < 3 or gray.shape[1] < 3:
        return 0.0
    kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float32)
    windows = sliding_window_view(gray.astype(np.float32), (3, 3))
    conv = (windows * kernel).sum(axis=(-1, -2))
    return float(conv.var())


def check_resolution(img: Image.Image) -> CheckResult:
    w, h = img.size
    mp = (w * h) / 1_000_000
    if mp >= RECOMMENDED_MP:
        return CheckResult("Resolution", "pass",
                           f"{w}×{h} px  ·  {mp:.1f} MP")
    if mp >= MIN_MP:
        return CheckResult("Resolution", "pass",
                           f"{w}×{h} px  ·  {mp:.1f} MP (meets minimum; "
                           f"recommended ≥ {int(RECOMMENDED_MP)} MP)")
    return CheckResult("Resolution", "fail",
                       f"{w}×{h} px  ·  {mp:.1f} MP — below the "
                       f"{int(MIN_MP)} MP minimum")


def check_focus(img: Image.Image) -> CheckResult:
    """Detects 'blurred or out of focus' photos."""
    small = img.convert("L").resize((400, int(400 * img.size[1] / img.size[0])))
    var = _laplacian_variance(np.array(small))
    if var >= BLUR_WARN:
        return CheckResult("Sharp focus", "pass", f"focus score {var:.0f} (sharp)")
    if var >= BLUR_FAIL:
        return CheckResult("Sharp focus", "warn",
                           f"focus score {var:.0f} — borderline, may be soft")
    return CheckResult("Sharp focus", "fail",
                       f"focus score {var:.0f} — image appears blurred or out of focus")


def check_head_visibility(img: Image.Image) -> CheckResult:
    """Detects 'head cut off at the frame edge' using aspect-ratio as a proxy.

    Real bow-head photos from a phone or DSLR sit between 1:1 and 2:1. Banner
    crops from dealer websites are 3:1 or wider — that's almost always a sign
    the head is not fully framed.
    """
    w, h = img.size
    ratio = max(w, h) / min(w, h)
    if ratio <= ASPECT_WARN:
        return CheckResult("Head visibility", "pass",
                           f"aspect {ratio:.2f}:1 — head should fit fully")
    if ratio <= ASPECT_FAIL:
        return CheckResult("Head visibility", "warn",
                           f"aspect {ratio:.2f}:1 — head may not be centred")
    return CheckResult("Head visibility", "fail",
                       f"aspect {ratio:.2f}:1 — looks like a banner crop, "
                       f"head likely cut off at the frame edge")


def check_glare(img: Image.Image) -> CheckResult:
    """Detects 'heavy glare covers the wood grain' via saturated-pixel fraction."""
    g = np.array(img.convert("L"))
    sat = float(np.mean(g >= 245))
    pct = sat * 100
    if sat < GLARE_WARN:
        return CheckResult("Glare", "pass",
                           f"{pct:.1f}% saturated highlights")
    if sat < GLARE_FAIL:
        return CheckResult("Glare", "warn",
                           f"{pct:.1f}% saturated highlights — some glare present")
    return CheckResult("Glare", "fail",
                       f"{pct:.1f}% saturated highlights — heavy glare covers the wood grain")


# ---------------------------------------------------------------------------
# Top-level
# ---------------------------------------------------------------------------


def preflight(image_bytes: bytes) -> PreflightReport:
    img = Image.open(io.BytesIO(image_bytes))
    img.load()

    checks = [
        check_resolution(img),
        check_focus(img),
        check_head_visibility(img),
        check_glare(img),
    ]

    if any(c.status == "fail" for c in checks):
        overall: Status = "fail"
    elif any(c.status == "warn" for c in checks):
        overall = "warn"
    else:
        overall = "pass"

    return PreflightReport(overall=overall, checks=checks)


# ---------------------------------------------------------------------------
# UI helpers
# ---------------------------------------------------------------------------


def status_emoji(status: Status) -> str:
    return {"pass": "✓", "warn": "!", "fail": "✕"}[status]


def status_color(status: Status) -> str:
    return {"pass": "#38761D", "warn": "#A8633D", "fail": "#842029"}[status]
