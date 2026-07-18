"""
Build a mature, clean, minimalist terminal-style GitHub Stats Card SVG (860px wide).
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "..", "data", "contributions.json")
OUT_PATH = os.path.join(HERE, "..", "stats-card.svg")

W, H = 860, 240
PAD = 24
TITLEBAR_H = 32

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#8b949e"
INK = "#c9d1d9"
KEY = "#ffa657"      # warm accent
GREEN = "#3fb950"
ACCENT = "#58a6ff"  # clean blue
CYAN = "#22d3ee"


def main():
    total_contribs = 553
    current_streak = 20
    longest_streak = 20

    if os.path.exists(DATA_PATH):
        try:
            data = json.load(open(DATA_PATH))
            days = data.get("days", [])
            total_contribs = data.get("total_contributions", sum(d["count"] for d in days))
            cs = data.get("current_streak", {})
            ls = data.get("longest_streak", {})
            current_streak = cs.get("length", 20)
            longest_streak = ls.get("length", 20)
        except Exception:
            pass

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="'Courier New', Courier, monospace">
  <defs>
    <linearGradient id="cardBg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{BG2}" />
      <stop offset="100%" stop-color="{BG}" />
    </linearGradient>
  </defs>

  <!-- Clean Container -->
  <rect width="{W}" height="{H}" rx="10" fill="url(#cardBg)" />
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="none" stroke="{FRAME}" stroke-width="1" />

  <!-- Terminal Header -->
  <line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-width="1" />
  <circle cx="20" cy="16" r="5" fill="#ff5f56" />
  <circle cx="36" cy="16" r="5" fill="#ffbd2e" />
  <circle cx="52" cy="16" r="5" fill="#27c93f" />
  <text x="{W/2}" y="20" fill="{MUTED}" font-size="12" text-anchor="middle">199adarsh@github: ~$ analytics --summary</text>

  <!-- Main Metrics Grid (Left Column) -->
  <g transform="translate(30, 60)">
    <text x="0" y="0" fill="{ACCENT}" font-size="13" font-weight="700">&#8212; PERFORMANCE METRICS</text>

    <!-- Total Contributions -->
    <text x="0" y="32" fill="{KEY}" font-size="12.5" font-weight="700">Total Contributions</text>
    <text x="210" y="32" fill="{GREEN}" font-size="14" font-weight="700">{total_contribs:,}</text>

    <!-- Longest Streak -->
    <text x="0" y="62" fill="{KEY}" font-size="12.5" font-weight="700">Longest Streak</text>
    <text x="210" y="62" fill="{CYAN}" font-size="13" font-weight="700">{longest_streak} days</text>

    <!-- Current Streak -->
    <text x="0" y="92" fill="{KEY}" font-size="12.5" font-weight="700">Current Streak</text>
    <text x="210" y="92" fill="{GREEN}" font-size="13" font-weight="700">{current_streak} days</text>
  </g>

  <!-- Divider Line -->
  <line x1="380" y1="52" x2="380" y2="180" stroke="{FRAME}" stroke-dasharray="4,4" />

  <!-- Tech Stack Share (Right Column) -->
  <g transform="translate(410, 60)">
    <text x="0" y="0" fill="{ACCENT}" font-size="13" font-weight="700">&#8212; CORE STACK SHARE</text>

    <!-- Java 45% -->
    <text x="0" y="32" fill="{INK}" font-size="12.5" font-weight="700">Java</text>
    <text x="75" y="32" fill="{MUTED}" font-size="12">[==================                  ]</text>
    <text x="375" y="32" fill="{INK}" font-size="12.5" font-weight="700">45%</text>

    <!-- React 35% -->
    <text x="0" y="62" fill="{INK}" font-size="12.5" font-weight="700">React</text>
    <text x="75" y="62" fill="{MUTED}" font-size="12">[==============                      ]</text>
    <text x="375" y="62" fill="{INK}" font-size="12.5" font-weight="700">35%</text>

    <!-- C++ 20% -->
    <text x="0" y="92" fill="{INK}" font-size="12.5" font-weight="700">C++</text>
    <text x="75" y="92" fill="{MUTED}" font-size="12">[========                            ]</text>
    <text x="375" y="92" fill="{INK}" font-size="12.5" font-weight="700">20%</text>
  </g>

  <!-- Clean Footer Bar -->
  <line x1="0" y1="{H-32}" x2="{W}" y2="{H-32}" stroke="{FRAME}" stroke-width="1" />
  <text x="30" y="{H-12}" fill="{GREEN}" font-size="12">&#9679; Status: Building &amp; Shipping</text>
  <text x="{W-30}" y="{H-12}" fill="{MUTED}" font-size="12" text-anchor="end">Auto-Refreshed Daily</text>
</svg>
"""

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT_PATH} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
