"""
Build an Awwwards-level 3D glassmorphic GitHub Stats Card SVG (860px wide)
with 3D bevels, metallic gradients, glowing neon counters, and stack percentages (Java, React, C++).
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "..", "data", "contributions.json")
OUT_PATH = os.path.join(HERE, "..", "stats-card.svg")

W, H = 860, 310

def main():
    total_contribs = 553
    current_streak = 20
    longest_streak = 20
    best_day_count = 44

    if os.path.exists(DATA_PATH):
        try:
            data = json.load(open(DATA_PATH))
            days = data.get("days", [])
            total_contribs = data.get("total_contributions", sum(d["count"] for d in days))
            best = data.get("best_day", {})
            best_day_count = best.get("count", 44)
            cs = data.get("current_streak", {})
            ls = data.get("longest_streak", {})
            current_streak = cs.get("length", 20)
            longest_streak = ls.get("length", 20)
        except Exception:
            pass

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="'Courier New', Courier, monospace">
  <defs>
    <!-- Background Gradients -->
    <linearGradient id="bgGlow" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="50%" stop-color="#090d16" />
      <stop offset="100%" stop-color="#05070c" />
    </linearGradient>

    <linearGradient id="glassBorder" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.8" />
      <stop offset="50%" stop-color="#818cf8" stop-opacity="0.3" />
      <stop offset="100%" stop-color="#c084fc" stop-opacity="0.6" />
    </linearGradient>

    <!-- Card 3D Bevel Gradients -->
    <linearGradient id="cardBevel" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#1e293b" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#0f172a" stop-opacity="0.9" />
    </linearGradient>

    <linearGradient id="javaGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff7b00" />
      <stop offset="100%" stop-color="#ffae00" />
    </linearGradient>

    <linearGradient id="reactGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00d2ff" />
      <stop offset="100%" stop-color="#3a7bd5" />
    </linearGradient>

    <linearGradient id="cppGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ec4899" />
      <stop offset="100%" stop-color="#8b5cf6" />
    </linearGradient>

    <!-- Glow Filters -->
    <filter id="neonGlowGreen" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <filter id="neonGlowBlue" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <filter id="shadow3d" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#000000" flood-opacity="0.75" />
    </filter>
  </defs>

  <!-- Outer Glass Frame with 3D Shadow -->
  <rect x="10" y="10" width="{W-20}" height="{H-20}" rx="16" fill="url(#bgGlow)" filter="url(#shadow3d)" />
  <rect x="10.5" y="10.5" width="{W-21}" height="{H-21}" rx="15.5" fill="none" stroke="url(#glassBorder)" stroke-width="1.5" />

  <!-- 3D Header Bar -->
  <rect x="11" y="11" width="{W-22}" height="36" rx="15" fill="#1e293b" fill-opacity="0.6" />
  <line x1="10" y1="47" x2="{W-10}" y2="47" stroke="#334155" stroke-opacity="0.5" />

  <!-- Mac Window Dots -->
  <circle cx="32" cy="29" r="5" fill="#ff5f56" />
  <circle cx="48" cy="29" r="5" fill="#ffbd2e" />
  <circle cx="64" cy="29" r="5" fill="#27c93f" />

  <text x="{W/2}" y="33" fill="#94a3b8" font-size="12" font-weight="700" text-anchor="middle" letter-spacing="1.5">199adarsh // EXECUTIVE ANALYTICS</text>

  <!-- 3D Stat Cards Section (3 Main Highlighted Counter Boxes) -->
  <!-- Box 1: Total Contributions -->
  <g transform="translate(30, 65)">
    <rect width="245" height="95" rx="12" fill="url(#cardBevel)" stroke="#334155" stroke-width="1" filter="url(#shadow3d)" />
    <rect width="245" height="4" rx="2" fill="#22c55e" filter="url(#neonGlowGreen)" />
    <text x="16" y="30" fill="#94a3b8" font-size="11" font-weight="700" letter-spacing="1">TOTAL CONTRIBUTIONS</text>
    <text x="16" y="68" fill="#4ade80" font-size="32" font-weight="900" filter="url(#neonGlowGreen)">{total_contribs:,}</text>
    <text x="145" y="66" fill="#64748b" font-size="11">in last 12 mos</text>
  </g>

  <!-- Box 2: Max Streak -->
  <g transform="translate(307, 65)">
    <rect width="245" height="95" rx="12" fill="url(#cardBevel)" stroke="#334155" stroke-width="1" filter="url(#shadow3d)" />
    <rect width="245" height="4" rx="2" fill="#38bdf8" filter="url(#neonGlowBlue)" />
    <text x="16" y="30" fill="#94a3b8" font-size="11" font-weight="700" letter-spacing="1">MAX STREAK</text>
    <text x="16" y="68" fill="#38bdf8" font-size="32" font-weight="900" filter="url(#neonGlowBlue)">{longest_streak}</text>
    <text x="110" y="66" fill="#38bdf8" font-size="14" font-weight="700">DAYS</text>
    <text x="165" y="66" fill="#64748b" font-size="11">(Best: {best_day_count}/day)</text>
  </g>

  <!-- Box 3: Current Streak -->
  <g transform="translate(585, 65)">
    <rect width="245" height="95" rx="12" fill="url(#cardBevel)" stroke="#334155" stroke-width="1" filter="url(#shadow3d)" />
    <rect width="245" height="4" rx="2" fill="#a855f7" filter="url(#neonGlowGreen)" />
    <text x="16" y="30" fill="#94a3b8" font-size="11" font-weight="700" letter-spacing="1">CURRENT STREAK</text>
    <text x="16" y="68" fill="#c084fc" font-size="32" font-weight="900" filter="url(#neonGlowBlue)">{current_streak}</text>
    <text x="110" y="66" fill="#c084fc" font-size="14" font-weight="700">DAYS</text>
    <text x="175" y="66" fill="#22c55e" font-size="11" font-weight="700">&#9679; ACTIVE</text>
  </g>

  <!-- Language Stack Share Bar (Java, React, C++) -->
  <g transform="translate(30, 185)">
    <rect width="800" height="95" rx="12" fill="url(#cardBevel)" stroke="#334155" stroke-width="1" />
    <text x="18" y="26" fill="#f8fafc" font-size="12" font-weight="700" letter-spacing="1">&#9889; CORE TECH STACK DISTRIBUTION</text>

    <!-- Progress Bar Frame -->
    <rect x="18" y="38" width="764" height="14" rx="7" fill="#0f172a" stroke="#1e293b" />
    
    <!-- Progress Bar Segments: Java (45%), React (35%), C++ (20%) -->
    <rect x="18" y="38" width="343.8" height="14" rx="7" fill="url(#javaGrad)" />
    <rect x="361.8" y="38" width="267.4" height="14" rx="0" fill="url(#reactGrad)" />
    <rect x="629.2" y="38" width="152.8" height="14" rx="7" fill="url(#cppGrad)" />

    <!-- Badges & Percentages Below Bar -->
    <!-- Java -->
    <circle cx="26" cy="72" r="5" fill="#ff7b00" />
    <text x="38" y="76" fill="#f8fafc" font-size="12" font-weight="700">JAVA</text>
    <text x="82" y="76" fill="#ffae00" font-size="12" font-weight="900">45%</text>

    <!-- React -->
    <circle cx="300" cy="72" r="5" fill="#00d2ff" />
    <text x="312" y="76" fill="#f8fafc" font-size="12" font-weight="700">REACT</text>
    <text x="365" y="76" fill="#38bdf8" font-size="12" font-weight="900">35%</text>

    <!-- C++ -->
    <circle cx="580" cy="72" r="5" fill="#ec4899" />
    <text x="592" y="76" fill="#f8fafc" font-size="12" font-weight="700">C++</text>
    <text x="630" y="76" fill="#c084fc" font-size="12" font-weight="900">20%</text>
  </g>

</svg>
"""
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT_PATH} ({len(svg)} bytes)")

if __name__ == "__main__":
    main()
