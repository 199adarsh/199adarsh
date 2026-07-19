#!/usr/bin/env python3
"""
Render data/contributions.json as a GitHub-style contribution heatmap SVG:
a grid of rounded, colored BOXES in the 53-week x 7-day calendar.
"""
import datetime
import json
import os

HERE = os.path.dirname(__file__)
IN_PATH = os.path.join(HERE, "..", "data", "contributions.json")
OUT_PATH = os.path.join(HERE, "..", "contrib-heatmap.svg")

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

CELL = 20
GAP = 5
STEP = CELL + GAP
PAD = 24
LEFT_LABEL_W = 35
TOP_LABEL_H = 24
TITLEBAR_H = 32

BG = "#0a0e14"
BG2 = "#0d1420"
FRAME = "#1f6feb"
MUTED = "#7d8590"
TEXT = "#e6edf3"
ACCENT = "#22d3ee"
GREEN = "#39d353"
GOLD = "#f2cc60"

COL_T = 0.018
ROW_T = 0.045
CELL_DUR = 0.42


def level_for(count):
    if count == 0:
        return 0
    if count <= 5:
        return 1
    if count <= 15:
        return 2
    if count <= 30:
        return 3
    if count <= 50:
        return 4
    return 5


def build_grid(days):
    first = datetime.date.fromisoformat(days[0]["date"])
    lead_pad = (first.weekday() + 1) % 7
    grid = []
    col = [None] * lead_pad

    for d in days:
        date = datetime.date.fromisoformat(d["date"])
        weekday = (date.weekday() + 1) % 7
        while len(col) < weekday:
            col.append(None)
        col.append((d["date"], d["count"], level_for(d["count"])))
        if len(col) == 7:
            grid.append(col)
            col = []

    if col:
        while len(col) < 7:
            col.append(None)
        grid.append(col)

    return grid


def render(data):
    today = datetime.date.today()
    start = today - datetime.timedelta(days=370)  # ~53 weeks

    days = [
        d for d in data["days"]
        if start <= datetime.date.fromisoformat(d["date"]) <= today
    ]
    if not days:
        days = data["days"]

    days = sorted(days, key=lambda d: d["date"])
    grid = build_grid(days)
    n_cols = len(grid)
    art_w = n_cols * STEP
    art_h = 7 * STEP

    month_labels = []
    seen_months = set()
    for ci, column in enumerate(grid):
        for cell in column:
            if cell is None:
                continue
            date = datetime.date.fromisoformat(cell[0])
            key = (date.year, date.month)
            if key not in seen_months and date.day <= 7:
                seen_months.add(key)
                month_labels.append((ci, date.strftime("%b")))
            break

    canvas_w = PAD + LEFT_LABEL_W + art_w + PAD
    stats_h = 88
    canvas_h = TITLEBAR_H + TOP_LABEL_H + art_h + stats_h + PAD

    css = f"""
@keyframes appear {{
  from {{
    opacity: 0;
    transform: scale(0.96);
  }}
  to {{
    opacity: 1;
    transform: scale(1);
  }}
}}

@keyframes breathe {{
  0%, 100% {{
    filter: brightness(1);
  }}
  50% {{
    filter: brightness(1.08);
  }}
}}

@keyframes frameGlow {{
  0%, 100% {{
    stroke-opacity: 0.45;
  }}
  50% {{
    stroke-opacity: 0.65;
  }}
}}

@keyframes titlePulse {{
  0%, 100% {{
    opacity: 0.82;
  }}
  50% {{
    opacity: 1;
  }}
}}

@keyframes legendPulse {{
  0%, 100% {{
    opacity: 0.9;
  }}
  50% {{
    opacity: 1;
  }}
}}

.c {{
  transform-origin: center;
  opacity: 0;
  transition: transform 180ms ease, filter 180ms ease;
}}

.active {{
  animation:
    appear {CELL_DUR:.2f}s cubic-bezier(.2,.9,.2,1) forwards,
    breathe 6.4s ease-in-out infinite;
}}

.inactive {{
  animation: appear {CELL_DUR:.2f}s cubic-bezier(.2,.9,.2,1) forwards;
}}

.c:hover {{
  transform: scale(1.06);
  filter: brightness(1.15);
}}

.frame {{
  animation: frameGlow 8s ease-in-out infinite;
}}

.title {{
  animation: titlePulse 7s ease-in-out infinite;
}}

.legend-rect {{
  animation: legendPulse 7.5s ease-in-out infinite;
}}
""".strip()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" '
        f'viewBox="0 0 {canvas_w} {canvas_h}" font-family="\'Courier New\', Courier, monospace">',
        f'<style>{css}</style>',
        '<defs>'
        f'<linearGradient id="hbg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient>'
        '</defs>',
        f'<rect width="{canvas_w}" height="{canvas_h}" rx="12" fill="url(#hbg)"/>',
        f'<rect x="0.5" y="0.5" width="{canvas_w-1}" height="{canvas_h-1}" rx="12" '
        f'fill="none" stroke="{FRAME}" stroke-width="1" class="frame"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{canvas_w}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-opacity="0.35"/>',
    ]

    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

    parts.append(
        f'<text x="{canvas_w/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
        f'class="title" text-anchor="middle">199adarsh@github: ~/contributions --graph</text>'
    )

    grid_top = TITLEBAR_H + TOP_LABEL_H
    grid_left = PAD + LEFT_LABEL_W

    for ci, label in month_labels:
        x = grid_left + ci * STEP
        parts.append(f'<text x="{x}" y="{TITLEBAR_H + 14}" fill="{MUTED}" font-size="10">{label}</text>')

    for wi, wname in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        y = grid_top + wi * STEP + CELL * 0.78
        parts.append(f'<text x="{PAD}" y="{y:.1f}" fill="{MUTED}" font-size="9">{wname}</text>')

    # the rest of the SVG rendering continues in Part 2

    for ci, column in enumerate(grid):
        gx = grid_left + ci * STEP
        for ri, cell in enumerate(column):
            if cell is None:
                continue

            date_s, count, lvl = cell
            gy = grid_top + ri * STEP
            delay = ci * COL_T + ri * ROW_T
            plural = "s" if count != 1 else ""
            cls = "c active" if lvl > 0 else "c inactive"

            parts.append(
                f'<rect class="{cls}" x="{gx}" y="{gy}" width="{CELL}" height="{CELL}" rx="2.5" '
                f'fill="{PALETTE[lvl]}" '
                f'style="animation-delay:{delay:.3f}s, {delay * 0.18:.3f}s">'
                f'<title>{date_s}: {count} contribution{plural}</title></rect>'
            )

    leg_y = grid_top + art_h + 6
    leg_x = canvas_w - PAD - (len(PALETTE) * (CELL - 1) + 70)

    parts.append(
        f'<text x="{leg_x}" y="{leg_y + CELL*0.8:.1f}" fill="{MUTED}" font-size="10" text-anchor="end">'
        f'Less</text>'
    )

    lx = leg_x + 8
    for lvl, color in enumerate(PALETTE):
        parts.append(
            f'<rect class="legend-rect" x="{lx}" y="{leg_y}" width="{CELL-1}" height="{CELL-1}" '
            f'rx="2.2" fill="{color}" style="animation-delay:{lvl * 0.22:.2f}s"/>'
        )
        lx += CELL

    parts.append(
        f'<text x="{lx + 4}" y="{leg_y + CELL*0.8:.1f}" fill="{MUTED}" font-size="10">'
        f'More</text>'
    )

    sep_y = leg_y + CELL + 14
    parts.append(
        f'<line x1="0" y1="{sep_y}" x2="{canvas_w}" y2="{sep_y}" stroke="{FRAME}" stroke-opacity="0.25"/>'
    )

    total = sum(d["count"] for d in days)
    best = max(days, key=lambda d: d["count"])
    start_date = days[0]["date"]
    end_date = days[-1]["date"]

    run = longest = 0
    cur = 0
    for d in days:
        if d["count"] > 0:
            run += 1
            if run > longest:
                longest = run
        else:
            run = 0
    cur = run

    ly = sep_y + 24
    parts.append(
        f'<text x="{PAD}" y="{ly}" font-size="13" fill="{GREEN}">'
        f'<tspan font-weight="700">{total:,}</tspan>'
        f'<tspan fill="{MUTED}"> contributions ({start.strftime("%b %Y")} &#8594; '
        f'{today.strftime("%b %Y")})</tspan></text>'
    )
    parts.append(
        f'<text x="{canvas_w - PAD}" y="{ly}" font-size="12" fill="{MUTED}" text-anchor="end">'
        f'{start_date} &#8594; {end_date}</text>'
    )

    ly += 24
    parts.append(
        f'<text x="{PAD}" y="{ly}" font-size="13" fill="{MUTED}">current streak '
        f'<tspan fill="{ACCENT}" font-weight="700">{cur} days</tspan>'
        f'<tspan fill="{MUTED}">   &#183;   longest </tspan>'
        f'<tspan fill="{ACCENT}" font-weight="700">{longest} days</tspan></text>'
    )
    parts.append(
        f'<text x="{canvas_w - PAD}" y="{ly}" font-size="12" fill="{MUTED}" text-anchor="end">'
        f'best day <tspan fill="{GOLD}" font-weight="700">{best["count"]}</tspan> on {best["date"]}</text>'
    )

    parts.append("</svg>")
    return "".join(parts)


if __name__ == "__main__":
    data = json.load(open(IN_PATH))
    svg = render(data)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT_PATH} ({len(svg)} bytes)")
