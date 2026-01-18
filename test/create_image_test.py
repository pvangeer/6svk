from svgwrite import Drawing
from svk.visualization import add_time_headers, add_group
from svk.visualization.helpers import color_toward_grey, wrapped_text, measure_text, wrapped_lines
from svk.io import svg_to_pdf
import math


def test_create_image():
    column_width = 650
    n_columns = 3
    column_header_height = 80
    paper_margin = 20
    arrow_depth = column_header_height / 4

    group_header_height = column_header_height / 2

    dwg = Drawing(size=(f"{paper_margin * 2 + column_width * n_columns}px", "800px"))

    add_time_headers(dwg, paper_margin, column_width, column_header_height)

    arrow_depth = round(group_header_height / 2)

    orange = (237, 113, 39)
    y_group1 = 2 * paper_margin + column_header_height
    group_header_height = 40
    group_width = round(column_width - arrow_depth)
    text_margin = 5

    add_group(
        dwg,
        id="group1",
        x=paper_margin,
        y=y_group1,
        width=group_width,
        height=600,
        color=color_toward_grey(orange, grey_fraction=0),
        header="Test groep",
        arrow_depth=arrow_depth,
        group_header_height=group_header_height,
    )

    text = "Dit is een voorbeeld van een te lange vraag die niet op de regel past en zou moeten worden gewrapped. We moeten de tekst alleen wel wat langer maken, anders wil wrappen nog niet lukken."
    (w, h) = measure_text(text, 12)

    x = paper_margin + arrow_depth + paper_margin
    y = y_group1 + group_header_height + paper_margin

    width = group_width - arrow_depth - 2 * paper_margin
    n_lines = math.ceil(w / width)
    height = h * n_lines * 1.2 + text_margin * 2

    dwg.add(dwg.rect(insert=(x, y), size=(width, height), stroke_width=0.5, fill="white", stroke="black"))
    lines = wrapped_lines(text=text, max_width=width - paper_margin)
    dwg.add(wrapped_text(dwg, lines=lines, insert=(x + text_margin, y + paper_margin / 2 + text_margin)))

    add_group(
        dwg,
        id="group2",
        x=paper_margin + column_width,
        y=2 * paper_margin + column_header_height,
        width=round(column_width - arrow_depth),
        height=600,
        color=color_toward_grey(orange, grey_fraction=0.5),
        header="Test groep",
        arrow_depth=arrow_depth,
    )

    add_group(
        dwg,
        id="group3",
        x=paper_margin + 2 * column_width,
        y=2 * paper_margin + column_header_height,
        width=round(column_width - arrow_depth),
        height=600,
        color=color_toward_grey(orange, grey_fraction=0.8),
        header="Test groep",
        arrow_depth=arrow_depth,
    )

    pt = "C:/test/Kennisagenda.pdf"
    svg_to_pdf(dwg, pt)
