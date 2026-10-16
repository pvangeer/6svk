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

from pydantic import ConfigDict
from svk.data import Color, KnownColors
from svk.visualization.elements._visual_element import VisualElement
from svk.visualization.helpers._drawchevron import draw_half_chevron
from svk.visualization.helpers._color_helper import get_contrast_color


class Column(VisualElement):
    """
    Class that represents a Column.
    """

    model_config = ConfigDict(frozen=True)

    header_title: str
    """Header/title of the column"""
    header_subtitle: str
    """Subtitle of the columns header."""
    header_color: Color
    """Color of the column (used as shading and as stroke color)"""
    number: int

    def measure(self) -> None:
        self._width = self.layout_configuration.column_width
        self._height = self.layout_configuration.column_header_height

    def _draw(self, x: float, y: float):
        """
        Draws the header

        :param x: The x-position of the left upper corner of the header
        :type x: float
        :param y: The y-position of the left upper corner of the header
        :type y: float
        """

        if self.header_title == "":
            return

        self._dwg.add(
            draw_half_chevron(
                self._dwg,
                x=x,
                y=y,
                width=self.width,
                height=self.height,
                use_gradients=self.layout_configuration.use_gradients,
                color=self.header_color,
            )
        )
        y_column_header_text = y + self.layout_configuration.column_header_height / 2
        text_fill = str(KnownColors.Black) if self.layout_configuration.use_gradients else str(get_contrast_color(self.header_color))
        self._dwg.add(
            self._dwg.text(
                self.header_title,
                insert=(x + self.layout_configuration.arrow_depth + self.layout_configuration.intermediate_margin, y_column_header_text),
                font_size=self.layout_configuration.column_header_font_size,
                font_family="Arial",
                font_weight="bold",
                fill=text_fill,
                text_anchor="start",
                dominant_baseline="middle",
            )
        )
        if self.header_subtitle != "":
            self._dwg.add(
                self._dwg.text(
                    self.header_subtitle,
                    insert=(x + self.layout_configuration.column_width - self.layout_configuration.arrow_depth, y_column_header_text),
                    font_family="Arial",
                    font_size=self.layout_configuration.column_header_font_size,
                    font_weight="normal",
                    fill=text_fill,
                    text_anchor="end",
                    dominant_baseline="middle",
                )
            )
