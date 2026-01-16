from svk.visualization.helpers import wrapped_text


def add_group(
    dwg,
    id: str,
    x: int,
    y: int,
    width: int,
    height: int,
    color: str,
    header: str,
    arrow_depth: int,
    group_header_height: int = 40,
    header_margin: int = 10,
    header_font_size: int = 14,
):

    gradient_id = f"gradient_{id}"
    header_size = 30

    x_scale = width / header_size
    radial_grad = dwg.radialGradient(
        center=((x + 20) / x_scale, y),  # center in relative coords
        r=header_size,  # radius relative to box
        gradientUnits="userSpaceOnUse",
        id=gradient_id,
    )
    radial_grad.add_stop_color(0, color)  # center
    radial_grad.add_stop_color(1, "white")  # edge

    radial_grad["gradientTransform"] = f"scale({x_scale},1)"

    dwg.defs.add(radial_grad)

    points = [
        (x, y),
        (x + width, y),
        (x + width, y + height),
        (x + arrow_depth, y + height),
        (x + arrow_depth, y + group_header_height),
    ]

    polygon = dwg.polygon(points=points, stroke=color, fill=f"url(#{gradient_id})", stroke_width=0.5, id="test")
    dwg.add(polygon)

    dwg.add(
        wrapped_text(
            dwg,
            header,
            insert=(x + arrow_depth + header_margin, y + header_margin + header_font_size),
            max_width=width,
            font_size=header_font_size,
            font_weight="bold",
        )
    )
