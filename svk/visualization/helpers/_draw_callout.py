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


def draw_callout(
    dwg: Drawing,
    x: float,
    y: float,
    width: float,
    height: float,
    color: str,
    stroke_width: float = 0.5,
    arrow_height: float = 30.0,
    arrow_depth: float = 20,
):
    gradient_id = f"gradient_group_header_{str(uuid4())}"
    x_scale = width / arrow_height
    radial_grad = dwg.radialGradient(
        center=((x + 20) / x_scale, y),  # center in relative coords
        r=arrow_height,  # radius relative to box
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
        (x + arrow_depth, y + arrow_height),
    ]

    polygon = dwg.polygon(points=points, stroke=color, fill=f"url(#{gradient_id})", stroke_width=stroke_width, id=str(uuid4()))
    dwg.add(polygon)
