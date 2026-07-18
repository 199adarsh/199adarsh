"""
Build a custom neofetch / terminal-style GitHub Stats Card SVG (860px wide)
matching the exact design system (Courier New, terminal dots, dark gradient, glowing highlights).
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "..", "data", "contributions.json")
OUT_PATH = os.path.join(HERE, "..", "stats-card.svg")

W, H = 860, 260
PAD = 24
TITLEBAR_H = 32

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#1f6feb"
MUTED = "#7d8590"
INK = "#c9d1d9"
KEY = "#ffa657"      # orange
SECTION = "#58a6ff"  # blue
GREEN = "#3fb950"
ACCENT = "#22d3ee"
GOLD = "#f2cc60"


def main():
    total_contribs = 553
    current_streak = 20
    longest_streak = 20
    active_days = 81
    best_day_count = 44
    best_day_date = "2026-01-11"

    if os.path.exists(DATA_PATH):
        try:
            data = json.load(open(DATA_PATH))
            days = data.get("days", [])
            total_contribs = data.get("total_contributions", sum(d["count"] for d in days))
            active_days = data.get("active_days", sum(1 for d in days if d["count"] > 0))
            best = data.get("best_day", {})
            best_day_count = best.get("count", 44)
            best_day_date = best.get("date", "2026-01-11")
            cs = data.get("current_streak", {})
            ls = data.get("longest_streak", {})
            current_streak = cs.get("length", 20)
            longest_streak = ls.get("length", 20)
        except Exception:
            pass

    css = """
@keyframes fade {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}
.row { animation: fade 0.4s ease-out forwards; }
""".strip()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="\'Courier New\', Courier, monospace">',
        f'<style>{css}</style>',
        '<defs>',
        f'<linearGradient id="sbg" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient>',
        '</defs>',
        f'<rect width="{W}" height="{H}" rx="12" fill="url(#sbg)"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-opacity="0.5"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-opacity="0.3"/>',
    ]

    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

    parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
                 f'text-anchor="middle">199adarsh@github: ~$ github-analytics --summary</text>')

    # 3 Column Layout inside card
    # Col 1: Activity Stats (X=24, W=260)
    # Col 2: Streaks & Highlights (X=300, W=260)
    # Col 3: Tech Languages % Breakdown (X=580, W=250)

    y0 = TITLEBAR_H + 35

    # Section Headers
    parts.append(f'<text x="24" y="{y0}" fill="{SECTION}" font-size="13" font-weight="700">&#8212; ACTIVITY STATS</text>')
    parts.append(f'<line x1="170" y1="{y0-4}" x2="270" y2="{y0-4}" stroke="{FRAME}" stroke-opacity="0.6"/>')

    parts.append(f'<text x="300" y="{y0}" fill="{SECTION}" font-size="13" font-weight="700">&#8212; STREAKS &amp; IMPACT</text>')
    parts.append(f'<line x1="460" y1="{y0-4}" x2="550" y2="{y0-4}" stroke="{FRAME}" stroke-opacity="0.6"/>')

    parts.append(f'<text x="580" y="{y0}" fill="{SECTION}" font-size="13" font-weight="700">&#8212; TOP STACK SHARE</text>')
    parts.append(f'<line x1="730" y1="{y0-4}" x2="836" y2="{y0-4}" stroke="{FRAME}" stroke-opacity="0.6"/>')

    # Rows Data
    col1_rows = [
        ("Total Contribs", f"{total_contribs:,}", ACCENT),
        ("Active Days", f"{active_days} days", INK),
        ("Best Day", f"{best_day_count} ({best_day_date})", GOLD),
    ]

    col2_rows = [
        ("Current Streak", f"{current_streak} days", GREEN),
        ("Longest Streak", f"{longest_streak} days", GREEN),
        ("Live Users", "200+ active", ACCENT),
    ]

    col3_rows = [
        ("Java / Spring", "38%", "#f89820"),
        ("React / TS", "32%", "#61dafb"),
        ("Python / AI", "20%", "#3572A5"),
        ("C++ / C", "10%", "#f34b7d"),
    ]

    y = y0 + 32
    for k, v, col in col1_rows:
        parts.append(f'<text x="24" y="{y}" fill="{KEY}" font-size="12.5" font-weight="700">{html.escape(k)}</text>')
        parts.append(f'<text x="160" y="{y}" fill="{col}" font-size="12.5" font-weight="700">{html.escape(v)}</text>')
        y += 24

    y = y0 + 32
    for k, v, col in col2_rows:
        parts.append(f'<text x="300" y="{y}" fill="{KEY}" font-size="12.5" font-weight="700">{html.escape(k)}</text>')
        parts.append(f'<text x="440" y="{y}" fill="{col}" font-size="12.5" font-weight="700">{html.escape(v)}</text>')
        y += 24

    y = y0 + 32
    for lang, pct, col in col3_rows:
        parts.append(f'<circle cx="585" cy="{y-4}" r="4" fill="{col}"/>')
        parts.append(f'<text x="598" y="{y}" fill="{INK}" font-size="12.5">{html.escape(lang)}</text>')
        parts.append(f'<text x="836" y="{y}" fill="{col}" font-size="12.5" font-weight="700" text-anchor="end">{pct}</text>')
        y += 24

    # Footer line
    y_foot = H - 20
    parts.append(f'<line x1="24" y1="{y_foot-16}" x2="{W-24}" y2="{y_foot-16}" stroke="{FRAME}" stroke-opacity="0.3"/>')
    parts.append(f'<text x="24" y="{y_foot}" fill="{GREEN}" font-size="12">&#9679; Status: Active &amp; Building</text>')
    parts.append(f'<text x="{W-24}" y="{y_foot}" fill="{MUTED}" font-size="12" text-anchor="end">Auto-Refreshed Daily</text>')

    parts.append("</svg>")
    svg = "".join(parts)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT_PATH} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
