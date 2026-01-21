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

from ._measuretext import measure_text

from svgwrite import Drawing
from svgwrite.elementfactory import ElementBuilder


def wrapped_lines(
    text: str,
    max_width: float,
    font_size: int = 12,
) -> list[str]:
    words = text.split()
    lines = []
    line = ""
    for word in words:
        test_line = line + word + " "
        (w, _) = measure_text(test_line, font_size)
        if w > max_width:
            lines.append(line)
            line = word + " "
        else:
            line = test_line
    if line:
        lines.append(line)

    return lines


def wrapped_text(
    dwg: Drawing,
    lines: list[str],
    insert: tuple[float, float],
    line_height: float = 1.2,
    font_size: int = 12,
    font_family: str = "Arial",
    font_weight: str = "normal",
    text_anchor: str = "start",
    dominant_baseline: str = "middle",
) -> ElementBuilder:
    text_elem = dwg.text("", insert=insert, dominant_baseline=dominant_baseline)

    y = insert[1]

    for line in lines:
        text_elem.add(
            dwg.tspan(
                line,
                x=[insert[0]],
                y=[y],
                font_size=font_size,
                font_family=font_family,
                font_weight=font_weight,
                text_anchor=text_anchor,
            )
        )
        y += font_size * line_height

    return text_elem
