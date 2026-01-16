from ._measuretext import measure_text

from svgwrite import Drawing
from svgwrite.elementfactory import ElementBuilder


def wrapped_text(
    dwg: Drawing,
    text,
    insert,
    max_width,
    line_height=1.2,
    font_size: int = 12,
    font_family: str = "Arial",
    font_weight: str = "normal",
    horizontal_alignment: str = "start",
    dominant_baseline: str = "middle",
) -> ElementBuilder:
    text_elem = dwg.text("", insert=insert, dominant_baseline=dominant_baseline)

    words = text.split()
    line = ""
    y = insert[1]

    for word in words:
        test_line = line + word + " "
        (w, h) = measure_text(test_line, font_size)
        if w > max_width:
            tspan = dwg.tspan(line, x=[insert[0]], y=[y], font_size=font_size, font_family=font_family, font_weight=font_weight)
            text_elem.add(tspan)
            line = word + " "
            y += font_size * line_height
        else:
            line = test_line

    if line:
        text_elem.add(
            dwg.tspan(
                line,
                x=[insert[0]],
                y=[y],
                font_size=font_size,
                font_family=font_family,
                font_weight=font_weight,
                text_anchor=horizontal_alignment,
            )
        )

    return text_elem
