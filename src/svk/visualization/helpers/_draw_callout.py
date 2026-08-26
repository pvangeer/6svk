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
from svk.visualization.helpers._radial_gradient import create_radial_gradient


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
    gradient_center: float = 0.3,
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
    :param gradient_center: The location of the center of the radial gradient (horizontal, relative to the width). This needs to be in the range [0-1]
    :type gradient_center: float
    """

    if gradient_center > 1 or gradient_center < 0:
        raise ValueError

    gradient_id = create_radial_gradient(
        dwg=dwg, x=x + gradient_center * width, y=y, width=(1 - gradient_center) * width * 2, height=arrow_height * 2, color=color
    )

    points = [
        (x, y),
        (x + width, y),
        (x + width, y + height),
        (x + arrow_depth, y + height),
        (x + arrow_depth, y + arrow_height),
    ]

    polygon = dwg.polygon(points=points, stroke=color, fill=f"url(#{gradient_id})", stroke_width=stroke_width)
    dwg.add(polygon)
