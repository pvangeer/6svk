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
from svk.visualization.helpers._wrappedtext import measure_text


class IdElement(VisualElement):
    id: str
    is_link_target: bool = False
    is_link: bool = False
    page_number: int | None = None

    @property
    def width(self) -> float:
        return self.layout_configuration.question_id_box_width

    @property
    def height(self) -> float:
        return 2 * self.layout_configuration.small_margin + self.layout_configuration.font_size * 1.2

    def draw(self, dwg: Drawing, x: float, y: float):
        y_top = y + self.layout_configuration.small_margin
        dwg.add(
            dwg.text(
                self.id,
                insert=(x + self.width / 2.0, y_top),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                text_anchor="middle",
                dominant_baseline="text-before-edge",
            )
        )

        if self.page_number is None:
            return

        if self.is_link:
            text_w, _ = measure_text(text=self.id, font_size=self.layout_configuration.font_size)
            x_text_start = x + self.width / 2.0 - text_w / 2.0
            self.links_register.register_link(
                link_target=self.id,
                page_number=self.page_number,
                x=x_text_start,
                y=y_top,
                width=text_w,
                height=self.layout_configuration.font_size * 1.2,
            )

        if self.is_link_target:
            self.links_register.register_link_target(link_target=self.id, page_number=self.page_number, x=x, y=y)
