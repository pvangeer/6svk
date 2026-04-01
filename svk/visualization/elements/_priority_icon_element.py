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

from __future__ import annotations
from pydantic import model_validator, PrivateAttr
from svgwrite import Drawing
from svk.visualization.elements._visual_element import VisualElement
from svk.visualization.helpers._draw_priority_arrow import draw_priority_arrow


class PriorityIconElement(VisualElement):
    priority: int
    """The research question"""

    _height: float = PrivateAttr()
    _width: float = PrivateAttr()

    @property
    def height(self) -> float:
        return self._height

    @property
    def width(self) -> float:
        return self._width

    @model_validator(mode="after")
    def validate(self) -> PriorityIconElement:
        self._height = self.layout_configuration.priority_arrow_width + self.layout_configuration.intermediate_margin * 2
        self._width = self.layout_configuration.priority_arrow_width + self.layout_configuration.small_margin * 2
        return self

    def draw(self, dwg: Drawing, x: float, y: float):
        y_middle = y + self.height / 2.0
        x_arrows_left = x + self.layout_configuration.small_margin
        match self.priority:
            case 0:
                draw_priority_arrow(dwg, x=x_arrows_left, y=y_middle, width=self.layout_configuration.priority_arrow_width)
            case 1:
                draw_priority_arrow(
                    dwg,
                    x=x_arrows_left,
                    y=y_middle - 2.5,
                    width=self.layout_configuration.priority_arrow_width,
                )
                draw_priority_arrow(
                    dwg,
                    x=x_arrows_left,
                    y=y_middle + 2.5,
                    width=self.layout_configuration.priority_arrow_width,
                )
            case 2:
                draw_priority_arrow(
                    dwg,
                    x=x_arrows_left,
                    y=y_middle - 5,
                    width=self.layout_configuration.priority_arrow_width,
                )
                draw_priority_arrow(
                    dwg,
                    x=x_arrows_left,
                    y=y_middle,
                    width=self.layout_configuration.priority_arrow_width,
                )
                draw_priority_arrow(
                    dwg,
                    x=x_arrows_left,
                    y=y_middle + 5,
                    width=self.layout_configuration.priority_arrow_width,
                )
        pass
