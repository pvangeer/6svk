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

from pydantic import PrivateAttr
from svk.data import Color, KnownColors, Label
from svk.visualization.elements._visual_element import VisualElement
from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.helpers._draw_callout import draw_callout


class LegendReferenceElement(VisualElement):
    page_number: int
    color: Color

    _label_size: tuple[float, float] = PrivateAttr(default=(0.0, 0.0))

    def initialize(self) -> None:
        pass

    def measure(self) -> None:
        legend_label = self.translator.get_label(label=Label.LegendTitle)
        self._label_size = measure_text(
            text=legend_label,
            font_size=self.layout_configuration.font_size,
            font_family=self.layout_configuration.font_family,
            font_weight="bold",
        )
        self._width = self.layout_configuration.arrow_depth + self.layout_configuration.intermediate_margin * 2 + self._label_size[0]
        self._height = max(
            [
                self.layout_configuration.arrow_height,
                self.layout_configuration.disclamer_font_size * 1.2 + self.layout_configuration.small_margin * 2,
            ]
        )

    def _draw(self, x: float, y: float):
        draw_callout(
            dwg=self._dwg,
            x=x,
            y=y,
            width=self._width,
            height=self._height,
            stroke=self.color,
            header_fill=self.color,
            fill=KnownColors.White,
            stroke_width=1.0,
            arrow_height=self.layout_configuration.arrow_height,
            arrow_depth=self.layout_configuration.arrow_depth,
            use_gradients=self.layout_configuration.use_gradients,
        )

        legend_label = self.translator.get_label(label=Label.LegendTitle)

        x_start_text = x + self.layout_configuration.arrow_depth + self.layout_configuration.intermediate_margin
        y_top_text = y + self.height / 2 - self._label_size[1] / 2
        self._dwg.add(
            self._dwg.text(
                legend_label,
                insert=(
                    x_start_text,
                    y_top_text,
                ),
                dominant_baseline="hanging",
                text_anchor="start",
                fill="black",
                font_family=self.layout_configuration.font_family,
                font_weight="bold",
                text_decoration="normal",
                font_size=self.layout_configuration.font_size,
            )
        )
        self.links_register.register_link(
            link_target="#legend_page",
            x=x_start_text,
            y=y_top_text,
            width=self._label_size[0],
            height=self._label_size[1],
            page_number=self.page_number,
        )
