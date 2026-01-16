from svgwrite import Drawing


def chevron(
    dwg: Drawing,
    x: int,
    y: int,
    width: int,
    height: int,
    id: str,
    arrow_depth: int = 20,
    color: str = "blue",
    stroke_width: float = 0.5,
    header_size: int = 30,
    add_to_dwg: bool = True,
):

    x_scale = width / header_size
    gradient_id = f"gradient_{id}"

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
        (x + width - arrow_depth, y),
        (x + width, y + height / 2),
        (x + width - arrow_depth, y + height),
        (x, y + height),
        (x + arrow_depth, y + height / 2),
    ]
    polygon = dwg.polygon(points=points, stroke=color, fill=f"url(#{gradient_id})", stroke_width=stroke_width, id=id)

    if add_to_dwg:
        dwg.add(polygon)

    return polygon
