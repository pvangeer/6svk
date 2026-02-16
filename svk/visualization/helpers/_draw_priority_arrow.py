"""
Copyright (C) Stichting Deltares 2026. All rights reserved.

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


def draw_priority_arrow(dwg: Drawing, x: float, y: float, width: float, height: float = 5, stroke_color="black"):
    """
    This function draws a simple arror (directed upward) at the specified position.

    :param dwg: The svgwrite.Drawing object used to draw the arrow with.
    :type dwg: Drawing
    :param x: The x-position of the left of the arrow.
    :type x: float
    :param y: The y-position of the middle of the arrow.
    :type y: float
    :param width: The width of the arrow.
    :type width: float
    :param height: The height of the arrow.
    :type height: float
    :param stroke_color: The stroke color of the arrow.
    """
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
