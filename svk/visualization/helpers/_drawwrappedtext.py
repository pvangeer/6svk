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

from ._measuretext import measure_text

from svgwrite import Drawing
from svgwrite.elementfactory import ElementBuilder


def wrapped_lines(
    text: str,
    max_width: float,
    font_size: int = 12,
) -> list[str]:
    """
    Method that splits a string into lines that will not exceed a specified width. This method assumes the use of arial font.

    :param text: The text that should be split into lines
    :type text: str
    :param max_width: the maximum width of the lines once printed as svg text elements
    :type max_width: float
    :param font_size: the desired font size for the printed text
    :type font_size: int
    :return: A list of lines that don't exceed the specified maximum width
    :rtype: list[str]
    """
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
    font_style: str = "normal",
) -> ElementBuilder:
    """
    Creates an svg text element with lines for each text line in lines.

    :param dwg: The svgwrite.Drawing object to add the lines to
    :type dwg: Drawing
    :param lines: a list of lines that need to be printed (see also 'wrapped_lines')
    :type lines: list[str]
    :param insert: The insert (x,y) of the text
    :type insert: tuple[float, float]
    :param line_height: The line height of the text
    :type line_height: float
    :param font_size: The desired font size
    :type font_size: int
    :param font_family: The font family (if different from Arial, possibly the lines won't fit the maximum width)
    :type font_family: str
    :param font_style: The font style
    :type font_style: str
    :param font_weight: The font weight
    :type font_weight: str
    :param text_anchor: The text anchor
    :type text_anchor: str
    :param dominant_baseline: The dominant baseline
    :type dominant_baseline: str
    :return: An element builder object (svg text) to add to the svgwrite.Drawing
    :rtype: ElementBuilder
    """

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
                font_style=font_style,
            )
        )
        y += font_size * line_height

    return text_elem
