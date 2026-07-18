import os

def create_ascii_svg():
    ascii_art = [
        "       .---.       ",
        "      /     \\      ",
        "     |  O O  |     ",
        "     |   ^   |     ",
        "      \\  =- /      ",
        "       '---'       ",
        "    .---| |---.    ",
        "   /    | |    \\   ",
        "  /  |  | |  |  \\  ",
        " |   |  |_|  |   | ",
        " |   |       |   | "
    ]
    
    # Elegant terminal ASCII card
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" width="370" height="370" viewBox="0 0 370 370">
  <rect width="370" height="370" rx="8" fill="#0d1117" stroke="#30363d" stroke-width="1"/>
  <circle cx="20" cy="20" r="6" fill="#ff5f56"/>
  <circle cx="40" cy="20" r="6" fill="#ffbd2e"/>
  <circle cx="60" cy="20" r="6" fill="#27c93f"/>
  <text x="80" y="24" fill="#8b949e" font-size="13" font-family="monospace">199adarsh@ascii:~</text>
  <line x1="0" y1="40" x2="370" y2="40" stroke="#30363d" stroke-width="1"/>

  <g font-family="monospace" font-size="11" fill="#7ee787">
    <text x="30" y="80">      .----------------.      </text>
    <text x="30" y="98">     /  ADARSH HERWADE  \     </text>
    <text x="30" y="116">    |   ==============   |    </text>
    <text x="30" y="134">    |   [+] AI &amp; DS Eng  |    </text>
    <text x="30" y="152">    |   [+] Full Stack   |    </text>
    <text x="30" y="170">    |   [+] Java / React |    </text>
    <text x="30" y="188">     \                  /     </text>
    <text x="30" y="206">      '----------------'      </text>
    <text x="30" y="234">      __   ___   ___          </text>
    <text x="30" y="252">     /_ | / _ \ / _ \         </text>
    <text x="30" y="270">      | || (_) | (_) |        </text>
    <text x="30" y="288">      | | \__, |\__, |        </text>
    <text x="30" y="306">      |_|   /_/   /_/         </text>
    <text x="30" y="330" fill="#58a6ff">   github.com/199adarsh       </text>
  </g>
</svg>"""
    with open("adarsh-ascii.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)

if __name__ == "__main__":
    create_ascii_svg()
