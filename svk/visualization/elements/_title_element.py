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
from pydantic import PrivateAttr, model_validator
from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.elements._visual_element import VisualElement
from svk.data import Label


class TitleElement(VisualElement):
    title: Label

    _height: float = PrivateAttr()
    _width: float = PrivateAttr()

    @model_validator(mode="after")
    def validate(self):
        self._width = (
            self.layout_configuration.small_margin
            + measure_text(self.translator.get_label(self.title), self.layout_configuration.font_size)[0]
            + self.layout_configuration.small_margin
        )
        self._height = (
            self.layout_configuration.small_margin + self.layout_configuration.font_size * 1.2 + self.layout_configuration.small_margin
        )
        return self

    @property
    def height(self) -> float:
        return self._height

    @property
    def width(self) -> float:
        return self._width

    def draw(self, dwg: Drawing, x: float, y: float) -> None:
        dwg.add(
            dwg.text(
                self.translator.get_label(self.title),
                insert=(x + self.layout_configuration.small_margin, y + self.layout_configuration.small_margin),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                font_style="italic",
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )
