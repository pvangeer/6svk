from svk.visualization.helpers._drawchevron import chevron
from svk.visualization.helpers._drawwrappedtext import wrapped_text
from svk.visualization.helpers._greyfraction import color_toward_grey


def add_time_headers(
    dwg,
    paper_margin: int,
    column_width: int,
    column_header_height: int,
    column_header_font_size: int = 18,
    arrow_depth: int = 20,
    column_margin: int = 10,
    grey_fractions: list[float] = [0.0, 0.5, 0.8],
    color: tuple[int, int, int] = (18, 103, 221),
):
    x_column_1 = paper_margin
    x_column_2 = paper_margin + column_width
    x_column_3 = paper_margin + 2 * column_width

    x_offset_column_header_text = arrow_depth + column_margin

    y_column_header = paper_margin
    y_column_header_text = paper_margin + column_header_height / 2 + column_header_font_size / 2

    color_1 = color_toward_grey(color[0], color[1], color[2], grey_fraction=grey_fractions[0])
    color_2 = color_toward_grey(color[0], color[1], color[2], grey_fraction=grey_fractions[1])
    color_3 = color_toward_grey(color[0], color[1], color[2], grey_fraction=grey_fractions[2])
    dwg.add(chevron(dwg, x=x_column_1, y=y_column_header, width=column_width, height=column_header_height, id="nu", color=color_1))
    dwg.add(
        wrapped_text(
            dwg,
            "Nu",
            insert=(x_column_1 + x_offset_column_header_text, y_column_header_text),
            max_width=column_width / 2,
            font_size=column_header_font_size,
            font_weight="bold",
        )
    )
    dwg.add(chevron(dwg, x=x_column_2, y=y_column_header, width=column_width, height=column_header_height, id="boeggolf", color=color_2))
    dwg.add(
        wrapped_text(
            dwg,
            "Boeggolf",
            insert=(x_column_2 + x_offset_column_header_text, y_column_header_text),
            max_width=column_width / 2,
            font_size=column_header_font_size,
            font_weight="bold",
        )
    )
    dwg.add(
        wrapped_text(
            dwg,
            "(2033-2040)",
            insert=(x_column_3 - arrow_depth, y_column_header_text),
            max_width=column_width / 2,
            horizontal_alignment="end",
            font_size=column_header_font_size,
            font_weight="normal",
        )
    )

    dwg.add(chevron(dwg, x=x_column_3, y=y_column_header, width=column_width, height=column_header_height, id="toekomst", color=color_3))
    dwg.add(
        wrapped_text(
            dwg,
            "Toekomst",
            insert=(x_column_3 + x_offset_column_header_text, y_column_header_text),
            max_width=column_width / 2,
            font_size=column_header_font_size,
            font_weight="bold",
        )
    )
    dwg.add(
        wrapped_text(
            dwg,
            "(>2040)",
            insert=(x_column_3 + column_width - arrow_depth, y_column_header_text),
            max_width=column_width / 2,
            horizontal_alignment="end",
            font_size=column_header_font_size,
            font_weight="normal",
        )
    )
