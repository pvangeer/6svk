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
from svgwrite import Drawing
from svk.visualization.elements._visual_element import VisualElement


class IdElement(VisualElement):
    id: str
    """The research question"""

    @property
    def width(self) -> float:
        return self.layout_configuration.question_id_box_width

    @property
    def height(self) -> float:
        return 2 * self.layout_configuration.small_margin + self.layout_configuration.font_size * 1.2

    def draw(self, dwg: Drawing, x: float, y: float):
        dwg.add(
            dwg.text(
                self.id,
                insert=(x + self.width / 2.0, y + self.layout_configuration.small_margin),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                text_anchor="middle",
                dominant_baseline="text-before-edge",
            )
        )
        pass
