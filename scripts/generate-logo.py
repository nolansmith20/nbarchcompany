#!/usr/bin/env python3
"""Recreate the N.B. Arch Co. badge and horizontal wordmark as SVG.

Lettering is set in Jost Light (SIL Open Font License) and converted to
outlines, so the marks stay crisp without the font installed.

The script looks for the woff2 next to common caches, then downloads it.
Run from the repo root:

    python3 scripts/generate-logo.py
"""

from __future__ import annotations

import math
import urllib.request
from pathlib import Path

from fontTools.misc.transform import Transform
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / "public" / "brand"
FONT_URL = "https://cdn.jsdelivr.net/fontsource/fonts/jost@5.2.8/latin-300-normal.woff2"
FONT_CANDIDATES = [
    Path("/tmp/nb-fonts/jost-300.woff2"),
    ROOT / "node_modules" / "@fontsource" / "jost" / "files" / "jost-latin-300-normal.woff2",
]

# Deepened rose-gold so the mark reads on cream, not only on black.
INK = "#5e342c"
ARCH_STOPS = (("#a15c45", "0%"), ("#8f4e3c", "46%"), ("#6e3428", "100%"))


def font_path() -> Path:
    for candidate in FONT_CANDIDATES:
        if candidate.exists():
            return candidate
    dest = Path("/tmp/nb-fonts/jost-300.woff2")
    dest.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(FONT_URL, dest)
    return dest


def load_font(path: Path):
    font = TTFont(path)
    upem = font["head"].unitsPerEm
    cap = font["OS/2"].sCapHeight or int(upem * 0.70)
    return {
        "gs": font.getGlyphSet(),
        "cmap": font.getBestCmap(),
        "upem": upem,
        "cap": cap,
    }


def extra_gap(ch, nxt, size, track):
    if nxt is None:
        return 0.0
    if ch == " ":
        return size * 0.08
    if ch == ".":
        return size * 0.14
    if nxt == ".":
        return size * 0.03
    return size * 0.072 * track


def layout(fp, text, size, track):
    gs, cmap, upem = fp["gs"], fp["cmap"], fp["upem"]
    scale = size / upem
    glyphs = []
    x = 0.0
    for i, ch in enumerate(text):
        name = cmap[ord(ch)]
        adv = gs[name].width * scale
        glyphs.append((name, x))
        nxt = text[i + 1] if i + 1 < len(text) else None
        x += adv + extra_gap(ch, nxt, size, track)
    return glyphs, x


def text_paths(fp, text, size, origin_x, baseline, track):
    gs = fp["gs"]
    scale = size / fp["upem"]
    parts = []
    for name, x in layout(fp, text, size, track)[0]:
        pen = SVGPathPen(gs)
        transform = Transform(scale, 0, 0, -scale, origin_x + x, baseline)
        gs[name].draw(TransformPen(pen, transform))
        commands = pen.getCommands()
        if commands:
            parts.append(commands)
    return parts


def catenary(cx, base, half_w, height, n=90):
    lo, hi = 1e-3, half_w * 40
    for _ in range(80):
        a = (lo + hi) / 2
        rise = a * (math.cosh(half_w / a) - 1)
        if rise > height:
            lo = a
        else:
            hi = a
    a = (lo + hi) / 2
    pts = []
    for i in range(n + 1):
        x = -half_w + 2 * half_w * i / n
        y_up = height - (a * (math.cosh(x / a) - 1))
        pts.append((cx + x, base - y_up))
    d = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts)
    return d, pts


def gradient(gid, y0, y1):
    stops = "".join(
        f'<stop offset="{offset}" stop-color="{color}"/>' for color, offset in ARCH_STOPS
    )
    return (
        f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" '
        f'x1="0" y1="{y0:.2f}" x2="0" y2="{y1:.2f}">{stops}</linearGradient>'
    )


def lockup(fp, gid, circle):
    main = "N.B. ARCH CO."
    sub = "CUSTOM GOODS"
    main_size = 88
    sub_size = 23
    cx = 500
    main_w = layout(fp, main, main_size, 1)[1]
    sub_w = layout(fp, sub, sub_size, 3.15)[1]
    main_x = cx - main_w / 2
    main_base = 556
    sub_base = 652
    cap_px = sub_size * (fp["cap"] / fp["upem"])
    rule_y = sub_base - cap_px * 0.48
    rule_gap = 18
    rule_len = 86
    while rule_len > 36 and (rule_len * 2 + rule_gap * 2 + sub_w) > main_w * 0.96:
        rule_len -= 2
    group_w = rule_len * 2 + rule_gap * 2 + sub_w
    group_x = cx - group_w / 2
    sub_x = group_x + rule_len + rule_gap

    arch_hw, arch_h, arch_base, arch_stroke = 154, 108, 428, 6.0
    arch_d, pts = catenary(cx, arch_base, arch_hw, arch_h)
    foot_l, foot_r = pts[0][0], pts[-1][0]
    gap = 28
    line_l = main_x + 2
    line_r = main_x + main_w - 2
    hair = 2.2

    parts = [gradient(gid, arch_base - arch_h - 8, arch_base + 4)]
    if circle:
        parts.append(
            f'<circle cx="500" cy="500" r="448" fill="none" stroke="{INK}" stroke-width="2.45"/>'
        )
    parts.append(
        f'<path d="{arch_d}" fill="none" stroke="url(#{gid})" stroke-width="{arch_stroke}" '
        f'stroke-linecap="butt" stroke-linejoin="round"/>'
    )
    parts.append(
        f'<line x1="{line_l:.2f}" y1="{arch_base}" x2="{foot_l - gap:.2f}" y2="{arch_base}" '
        f'stroke="{INK}" stroke-width="{hair}"/>'
    )
    parts.append(
        f'<line x1="{foot_r + gap:.2f}" y1="{arch_base}" x2="{line_r:.2f}" y2="{arch_base}" '
        f'stroke="{INK}" stroke-width="{hair}"/>'
    )
    parts.append(
        "".join(
            f'<path fill="{INK}" d="{d}"/>'
            for d in text_paths(fp, main, main_size, main_x, main_base, 1)
        )
    )
    parts.append(
        "".join(
            f'<path fill="{INK}" d="{d}"/>'
            for d in text_paths(fp, sub, sub_size, sub_x, sub_base, 3.15)
        )
    )
    parts.append(
        f'<line x1="{group_x:.2f}" y1="{rule_y:.2f}" x2="{group_x + rule_len:.2f}" y2="{rule_y:.2f}" '
        f'stroke="{INK}" stroke-width="{hair}"/>'
    )
    right_rule = sub_x + sub_w + rule_gap
    parts.append(
        f'<line x1="{right_rule:.2f}" y1="{rule_y:.2f}" x2="{right_rule + rule_len:.2f}" y2="{rule_y:.2f}" '
        f'stroke="{INK}" stroke-width="{hair}"/>'
    )

    top = arch_base - arch_h - arch_stroke
    bottom = sub_base + 8
    left = min(line_l, group_x) - 4
    right = max(line_r, group_x + group_w) + 4
    return parts, (left, top, right, bottom), main_w


def svg_document(body, viewbox, title, desc):
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" role="img" '
        'aria-labelledby="title desc">\n'
        f'  <title id="title">{title}</title>\n'
        f'  <desc id="desc">{desc}</desc>\n'
        f"  {body}\n"
        "</svg>\n"
    )


def arch_only(size_note=""):
    d, _ = catenary(32, 46, 22, 20, n=64)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-labelledby="title">
  <title id="title">N.B. Arch Co. arch{size_note}</title>
  <rect width="64" height="64" rx="14" fill="#f7f1e8"/>
  {gradient("arch", 24, 48)}
  <path d="{d}" fill="none" stroke="url(#arch)" stroke-width="5.4" stroke-linecap="butt" stroke-linejoin="round"/>
</svg>
'''


def arch_transparent():
    d, _ = catenary(50, 58, 36, 34, n=64)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 64" fill="none" role="img" aria-hidden="true">
  <title>Arch mark</title>
  {gradient("arch", 20, 60)}
  <path d="{d}" stroke="url(#arch)" stroke-width="3.2" stroke-linecap="butt" stroke-linejoin="round"/>
</svg>
'''


def main():
    BRAND.mkdir(parents=True, exist_ok=True)
    fp = load_font(font_path())
    badge_parts, _, main_w = lockup(fp, "badgeArch", circle=True)
    badge = svg_document(
        "\n  ".join(badge_parts),
        "0 0 1000 1000",
        "N.B. Arch Co.",
        "Circular badge. A rose-gold Gateway Arch over N.B. ARCH CO. and the words Custom Goods, for light backgrounds.",
    )
    (BRAND / "logo-badge.svg").write_text(badge)

    word_parts, box, _ = lockup(fp, "wordArch", circle=False)
    left, top, right, bottom = box
    pad_x, pad_y = 8, 18
    width = (right - left) + pad_x * 2
    height = (bottom - top) + pad_y * 2
    body = (
        f'<g transform="translate({pad_x - left:.2f} {pad_y - top:.2f})">\n    '
        + "\n    ".join(word_parts)
        + "\n  </g>"
    )
    word = svg_document(
        body,
        f"0 0 {width:.2f} {height:.2f}",
        "N.B. Arch Co.",
        "Horizontal wordmark in deepened rose-gold, for light backgrounds.",
    )
    (BRAND / "logo-wordmark.svg").write_text(word)
    (ROOT / "public" / "favicon.svg").write_text(arch_only())
    (BRAND / "arch.svg").write_text(arch_transparent())
    print(f"main text width {main_w:.1f}")
    print(f"wordmark viewBox 0 0 {width:.2f} {height:.2f} aspect {width / height:.4f}")


if __name__ == "__main__":
    main()
