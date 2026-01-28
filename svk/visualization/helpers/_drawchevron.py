"""
Copyright (C) Stichting Deltares 2024. All rights reserved.

This file is part of the dikernel-python toolbox.

This program is free software; you can redistribute it and/or modify it under the terms of
the GNU Lesser General Public License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with this
program; if not, see <https://www.gnu.org/licenses/>.

All names, logos, and references to "Deltares" are registered trademarks of Stichting
Deltares and remain full property of Stichting Deltares at all times. All rights reserved.
"""

from svgwrite import Drawing
from uuid import uuid4


def draw_half_chevron(
    dwg: Drawing,
    x: int,
    y: int,
    width: int,
    height: int,
    arrow_depth: int = 20,
    color: str = "blue",
    stroke_width: float = 0.5,
    header_size: int = 30,
    add_to_dwg: bool = True,
):
    x_scale = width / header_size
    gradient_id = f"gradient_{str(uuid4())}"

    radial_grad = dwg.radialGradient(
        center=((x + 20) / x_scale, y),
        r=header_size,
        gradientUnits="userSpaceOnUse",
        id=gradient_id,
    )
    radial_grad.add_stop_color(0, color)
    radial_grad.add_stop_color(1, "white")

    radial_grad["gradientTransform"] = f"scale({x_scale},1)"

    dwg.defs.add(radial_grad)

    points = [
        (x, y),
        (x + width - arrow_depth, y),
        (x + width, y + height / 2),
        (x + width - arrow_depth, y + height),
        (x + arrow_depth, y + height),
        (x + arrow_depth, y + height / 2),
    ]
    polygon = dwg.polygon(points=points, stroke=color, fill=f"url(#{gradient_id})", stroke_width=stroke_width, id=str(uuid4()))

    if add_to_dwg:
        dwg.add(polygon)

    return polygon
