#!/usr/bin/env python3
"""Placeholder gallery plates. Swap the files, or point the HTML at photos."""

from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "public" / "gallery"
STROKE = "#8f4e3c"
BG = "#fffaf4"


def plate(name, label, body):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1000" role="img">
  <title>{label} — placeholder drawing</title>
  <rect width="800" height="1000" fill="{BG}"/>
  <g fill="none" stroke="{STROKE}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
    {body}
  </g>
</svg>
'''


def arch(cx, cy, w, h):
    """A small engraved arch with side ticks, centered on (cx, cy)."""
    hw = w / 2
    return f'''<path d="M {cx - hw:.1f} {cy:.1f} C {cx - hw:.1f} {cy - h:.1f}, {cx - hw * 0.15:.1f} {cy - h:.1f}, {cx:.1f} {cy - h:.1f} C {cx + hw * 0.15:.1f} {cy - h:.1f}, {cx + hw:.1f} {cy - h:.1f}, {cx + hw:.1f} {cy:.1f}"/>
    <path d="M {cx - hw - w * 0.28:.1f} {cy:.1f} H {cx - hw - 8:.1f}"/>
    <path d="M {cx + hw + 8:.1f} {cy:.1f} H {cx + hw + w * 0.28:.1f}"/>'''


PLATES = {}

PLATES["tumbler"] = (
    "Engraved tumbler",
    f'''
    <path d="M318 248 L338 760 Q400 802 462 760 L482 248"/>
    <ellipse cx="400" cy="248" rx="82" ry="16"/>
    <ellipse cx="400" cy="248" rx="68" ry="10"/>
    <path d="M326 248 L332 210 Q400 196 468 210 L474 248"/>
    <path d="M348 360 H452"/>
    <path d="M352 378 H448"/>
    {arch(400, 560, 86, 36)}
    ''',
)

PLATES["glass"] = (
    "Engraved rocks glass",
    f'''
    <path d="M250 390 L278 700 Q400 748 522 700 L550 390"/>
    <ellipse cx="400" cy="390" rx="150" ry="22"/>
    <ellipse cx="400" cy="390" rx="128" ry="14"/>
    <path d="M292 690 Q400 724 508 690"/>
    <path d="M300 718 Q400 754 500 718"/>
    {arch(400, 560, 92, 34)}
    ''',
)

PLATES["mug"] = (
    "Engraved mug",
    f'''
    <path d="M250 300 L272 690 Q360 742 448 690 L470 300"/>
    <ellipse cx="360" cy="300" rx="110" ry="20"/>
    <ellipse cx="360" cy="300" rx="92" ry="12"/>
    <path d="M470 390 C560 390, 572 560, 470 575"/>
    <path d="M470 424 C528 430, 534 530, 470 542"/>
    {arch(360, 520, 78, 32)}
    ''',
)

PLATES["flask"] = (
    "Engraved flask",
    f'''
    <rect x="352" y="168" width="96" height="36" rx="4"/>
    <path d="M368 204 H432 V248"/>
    <path d="M300 300 C250 340, 230 430, 236 560 C242 700, 300 760, 400 760 C500 760, 558 700, 564 560 C570 430, 550 340, 500 300 C470 278, 430 270, 400 270 C370 270, 330 278, 300 300 Z"/>
    <path d="M318 248 H482"/>
    <path d="M332 248 V278"/>
    <path d="M468 248 V278"/>
    {arch(400, 520, 90, 34)}
    ''',
)

PLATES["board"] = (
    "Engraved cutting board",
    f'''
    <rect x="338" y="148" width="124" height="140" rx="62"/>
    <circle cx="400" cy="200" r="15"/>
    <rect x="155" y="246" width="490" height="540" rx="22"/>
    <rect x="188" y="280" width="424" height="472" rx="12"/>
    {arch(400, 530, 120, 42)}
    ''',
)

PLATES["sign"] = (
    "Engraved sign",
    f'''
    <rect x="120" y="330" width="560" height="300" rx="6"/>
    <rect x="146" y="356" width="508" height="248" rx="2"/>
    {arch(400, 500, 150, 48)}
    ''',
)

PLATES["plaque"] = (
    "Engraved plaque",
    f'''
    <path d="M230 430 L230 760 Q400 820 570 760 L570 430 Q400 300 230 430 Z"/>
    <path d="M262 450 L262 742 Q400 790 538 742 L538 450 Q400 348 262 450 Z"/>
    {arch(400, 580, 100, 36)}
    <path d="M330 820 H470"/>
    <path d="M360 838 H440"/>
    ''',
)

PLATES["box"] = (
    "Engraved keepsake box",
    f'''
    <path d="M400 250 L590 345 L400 440 L210 345 Z"/>
    <path d="M210 345 L210 590 L400 685 L400 440"/>
    <path d="M590 345 L590 590 L400 685 L400 440"/>
    <path d="M400 250 L400 300"/>
    {arch(400, 360, 70, 26)}
    ''',
)

PLATES["corporate"] = (
    "Matched engraved tumblers",
    f'''
    <path d="M178 340 L196 690 Q250 724 304 690 L322 340"/>
    <ellipse cx="250" cy="340" rx="72" ry="14"/>
    <path d="M338 300 L360 700 Q430 742 500 700 L522 300"/>
    <ellipse cx="430" cy="300" rx="92" ry="16"/>
    <path d="M538 340 L556 690 Q610 724 664 690 L682 340"/>
    <ellipse cx="610" cy="340" rx="72" ry="14"/>
    <path d="M150 760 H690"/>
    {arch(250, 530, 52, 22)}
    {arch(430, 510, 64, 26)}
    {arch(610, 530, 52, 22)}
    ''',
)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, (label, body) in PLATES.items():
        (OUT / f"{slug}.svg").write_text(plate(slug, label, body))
        print(slug)


if __name__ == "__main__":
    main()
