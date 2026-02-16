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

import re
from svgwrite import Drawing


def draw_disclaimer(
    dwg: Drawing,
    disclaimer_text: str,
    insert: tuple[float, float],
    dominant_baseline: str = "hanging",
    text_anchor: str = "start",
    font_size: float = 12,
    links: list[tuple[str, str]] = [],
):
    """
    This function helps to draw a disclaimer. It replaces specific words in the specified text with links and draws it on a svgwrite.Drawing.

    :param dwg: The svgwrite.Drawing object that should contain the disclaimer.
    :type dwg: Drawing
    :param disclaimer_text: The actual disclaimer text.
    :type disclaimer_text: str
    :param insert: The insert (x,y) of the disclaimer (start position, see also text_anchor and dominant_baseline)
    :type insert: tuple[float, float]
    :param dominant_baseline: The dominant baseline, determines where the string is placed relative to the specified insert (see also svgwrite documentation).
    :type dominant_baseline: str
    :param text_anchor: The text_anchor, determines where the string is placed relative to the specified insert (see also svgwrite documentation).
    :type text_anchor: str
    :param font_size: The font size used to draw the text.
    :type font_size: float
    :param links: A description of the links that should replace text (first tuple value is a string that should be a hyperlink, second tuple value is the actual link it should refer to).
    :type links: list[tuple[str, str]]
    """
    pattern = f"({'|'.join(map(re.escape, [l[0] for l in links]))})"
    parts = re.split(pattern, disclaimer_text)

    disclaimer_text_element = dwg.text(
        parts[0],
        insert=insert,
        dominant_baseline=dominant_baseline,
        text_anchor=text_anchor,
        font_size=font_size,
    )

    for part in parts[1:]:
        link_tuple = next((t for t in links if t[0] == part), None)
        if link_tuple is not None:
            link = dwg.a(link_tuple[1])

            link.add(
                dwg.tspan(
                    link_tuple[0],
                    fill="blue",
                    text_decoration="underline",
                    cursor="pointer",
                )
            )

            disclaimer_text_element.add(link)
        else:
            disclaimer_text_element.add(dwg.tspan(part, font_size=font_size))

    dwg.add(disclaimer_text_element)
