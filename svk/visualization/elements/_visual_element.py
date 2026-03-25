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

from pydantic import BaseModel
from svk.data import LinksRegister, Translator
from svk.visualization._layout_configuration import LayoutConfiguration
from svgwrite import Drawing
from abc import ABC, abstractmethod


class VisualElement(BaseModel, ABC):
    layout_configuration: LayoutConfiguration
    """The layout configuration shared across all elements of a document."""
    links_register: LinksRegister
    translator: Translator

    # @abstractmethod
    # def get_size(self) -> tuple[float, float]:
    #     pass

    @abstractmethod
    def draw(self, dwg: Drawing, left: float, top: float) -> tuple[float, float]:
        pass

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
