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
from enum import Enum
from svk.visualization.elements._visual_element import VisualElement


class Alignment(Enum):
    TopLeft = 0
    TopCenter = 1
    TopRight = 2
    MiddleLeft = 3
    MiddleCenter = 4
    MiddleRight = 5
    BottomLeft = 6
    BottomCenter = 7
    BottomRight = 8


class VisualElementsContainer(VisualElement):
    def draw_vertical_separator(self, dwg: Drawing, x: float, y: float, element_height: float, color: str):
        dwg.add(
            dwg.line(
                start=(x, y + self.layout_configuration.small_margin),
                end=(x, y + element_height - self.layout_configuration.small_margin),
                stroke_width=0.5,
                stroke=color,
            )
        )

    def draw_horizontal_separator(self, dwg: Drawing, x: float, y: float, element_width: float, color: str):
        dwg.add(
            dwg.line(
                start=(x + self.layout_configuration.small_margin, y),
                end=(x + element_width - self.layout_configuration.small_margin, y),
                stroke_width=0.5,
                stroke=color,
            )
        )

    def draw_element(
        self,
        dwg: Drawing,
        element: VisualElement,
        x_container: float,
        y_container: float,
        width_container: float,
        height_container: float,
        alignment: Alignment = Alignment.TopLeft,
    ) -> None:
        x = x_container
        y = y_container
        match alignment:
            case Alignment.TopCenter:
                x = x_container + (width_container - element.width) / 2
            case Alignment.TopRight:
                x = x_container + (width_container - element.width)
            case Alignment.MiddleLeft:
                y = y_container + (height_container - element.height) / 2
            case Alignment.MiddleCenter:
                y = y_container + (height_container - element.height) / 2
                x = x_container + (width_container - element.width) / 2
            case Alignment.MiddleRight:
                y = y_container + (height_container - element.height) / 2
                x = x_container + (width_container - element.width)
            case Alignment.BottomLeft:
                y = y_container + (height_container - element.height)
            case Alignment.BottomCenter:
                y = y_container + (height_container - element.height)
                x = x_container + (width_container - element.width) / 2
            case Alignment.BottomRight:
                y = y_container + (height_container - element.height)
                x = x_container + (width_container - element.width)

        element.draw(dwg=dwg, x=x, y=y)
