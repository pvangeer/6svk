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
from svk.visualization.helpers._drawchevron import draw_half_chevron
from svk.visualization._visual_element import VisualElement


class Header(VisualElement):
    """
    Represents a column Header
    """

    title: str
    """The title of the header"""
    subtitle: str
    """the subtitle of the header"""
    color: str
    """The color of the header"""

    def get_height(self) -> float:
        return self.layout_configuration.column_header_height

    def draw(self, dwg: Drawing, x: float, y: float):
        """
        Draws the header

        :param dwg: The svgwrite.Drawing object used to draw the header
        :type dwg: Drawing
        :param x: The x-position of the left upper corner of the header
        :type x: float
        :param y: The y-position of the left upper corner of the header
        :type y: float
        """
        dwg.add(
            draw_half_chevron(
                dwg,
                x=x,
                y=y,
                width=self.layout_configuration.column_width,
                height=self.layout_configuration.column_header_height,
                color=self.color,
            )
        )
        y_column_header_text = y + self.layout_configuration.column_header_height / 2
        dwg.add(
            dwg.text(
                self.title,
                insert=(x + self.layout_configuration.arrow_depth + self.layout_configuration.intermediate_margin, y_column_header_text),
                font_size=self.layout_configuration.column_header_font_size,
                font_family="Arial",
                font_weight="bold",
                text_anchor="start",
                dominant_baseline="middle",
            )
        )
        if self.subtitle != "":
            dwg.add(
                dwg.text(
                    self.subtitle,
                    insert=(x + self.layout_configuration.column_width - self.layout_configuration.arrow_depth, y_column_header_text),
                    font_family="Arial",
                    text_anchor="end",
                    dominant_baseline="middle",
                    font_size=self.layout_configuration.column_header_font_size,
                    font_weight="normal",
                )
            )
