import json
import os

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def render_svg():
    if not os.path.exists("data/contributions.json"):
        return
    with open("data/contributions.json", "r") as f:
        data = json.load(f)
    days = data.get("days", [])
    cols, rows, box_size, gap = 53, 7, 10, 3
    width = cols * (box_size + gap) + 20
    height = rows * (box_size + gap) + 30
    rects = []
    for i, day in enumerate(days[:cols * rows]):
        c, r = i // rows, i % rows
        x, y = 10 + c * (box_size + gap), 10 + r * (box_size + gap)
        level = min(day.get("count", 0), len(PALETTE) - 1)
        rects.append(f'<rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" rx="2" fill="{PALETTE[level]}" />')
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <style>rect {{ transition: fill 0.3s; }}</style>
  <g>{''.join(rects)}</g>
</svg>'''
    with open("contrib-heatmap.svg", "w") as f:
        f.write(svg_content)

if __name__ == "__main__":
    render_svg()
