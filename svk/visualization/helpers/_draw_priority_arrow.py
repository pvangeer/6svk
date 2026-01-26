from svgwrite import Drawing


def draw_priority_arrow(dwg: Drawing, x: float, y: float, width: float, height: float = 5, stroke_color="black"):
    stroke_width = 3
    line1 = dwg.line(
        start=(x, y + height / 2),
        end=(x + width / 2, y - height / 2),
        stroke=stroke_color,
        stroke_width=stroke_width,
        stroke_linecap="round",
    )
    line2 = dwg.line(
        start=(x + width / 2, y - height / 2),
        end=(x + width, y + height / 2),
        stroke=stroke_color,
        stroke_width=stroke_width,
        stroke_linecap="round",
    )
    dwg.add(line1)
    dwg.add(line2)
