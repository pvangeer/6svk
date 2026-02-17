"""
Copyright (C) Stichting Deltares 2026. All rights reserved.

This file is part of the 6svk toolbox.

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
    """
    Draws a callout object and adds it to the drawing.

    :param dwg: The svgwrite.Drawing object the callout should be added to.
    :type dwg: Drawing
    :param x: The x-position (in points) of the left upper corner of the callout.
    :type x: float
    :param y: The y-position (in points) of the left upper corner of the callout.
    :type y: float
    :param width: The width (in points) of the callout.
    :type width: float
    :param height: The height (in points) of the callout.
    :type height: float
    :param color: The color of the callout.
    :type color: str
    :param stroke_width: The stroke with of the callout.
    :type stroke_width: float
    :param arrow_height: The height of the arrow of the callout.
    :type arrow_height: float
    :param arrow_depth: The depth of the arrow of the callout.
    :type arrow_depth: float
    """
    gradient_id = f"gradient_group_header_{str(uuid4())}"
    x_scale = width / arrow_height
    radial_grad = dwg.radialGradient(
        center=(
            (x + 20) / x_scale,
            y,
        ),  # TODO: Make the 20 configurable? Should we put generating a radial gradient into a separate function as it is done in multiple helper functions?
        r=arrow_height,
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
