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
from svk.data import StormSurgeBarrier, IconProvider
from svk.visualization.elements._visual_elements_container import VisualElementsContainer
from svk.visualization.helpers._draw_scaled_icon import draw_scaled_icon
from svk.visualization.helpers._measuretext import measure_text


class StormSurgeBarriersExeplanationLegendElement(VisualElementsContainer):
    _height: float = PrivateAttr()
    _width: float = PrivateAttr()
    _width_first_column: float = PrivateAttr()
    _width_second_column: float = PrivateAttr()
    _width_third_column: float = PrivateAttr()
    _row_height: float = PrivateAttr()

    _ssbs: tuple[tuple[StormSurgeBarrier, str], ...] = (
        (StormSurgeBarrier.MaeslantBarrier, "MLB"),
        (StormSurgeBarrier.HartelBarrier, "HK"),
        (StormSurgeBarrier.HaringvlietBarrier, "HV"),
        (StormSurgeBarrier.HollandseIJsselBarrier, "HIJK"),
        (StormSurgeBarrier.EasternScheldtBarrier, "OSK"),
        (StormSurgeBarrier.Ramspol, "RP"),
    )

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    @model_validator(mode="after")
    def validate(self) -> StormSurgeBarriersExeplanationLegendElement:
        self._width_first_column = max([measure_text(s[1])[0] for s in self._ssbs]) + 2 * self.layout_configuration.small_margin
        self._width_second_column = self.layout_configuration.icon_width_small + self.layout_configuration.small_margin
        self._width_third_column = (
            max([measure_text(self.translator.get_label(s[0].title))[0] for s in self._ssbs]) + +self.layout_configuration.small_margin
        )
        self._width = self._width_first_column + self._width_second_column + self._width_third_column
        self._row_height = self.layout_configuration.icon_width_small
        self._height = len(self._ssbs) * self._row_height + (len(self._ssbs) - 1) * self.layout_configuration.small_margin

        return self

    def _draw(self, x: float, y: float):
        y_top = y
        x_1 = x
        x_2 = x + self._width_first_column
        x_3 = x_2 + self._width_second_column
        for ssb in self._ssbs:
            icon = IconProvider.create_icon(ssb[0])
            if icon is None:
                continue

            self._dwg.add(
                self._dwg.text(
                    ssb[1],
                    insert=(x_1 + 0.5 * self._width_first_column, y_top + 0.5 * self._row_height),
                    font_size=self.layout_configuration.font_size,
                    font_family="Arial",
                    font_weight="normal",
                    font_style="normal",
                    text_anchor="middle",
                    dominant_baseline="middle",
                )
            )

            draw_scaled_icon(
                dwg=self._dwg,
                icon=icon,
                insert=(
                    x_2,
                    y_top,
                ),
                size=(self.layout_configuration.icon_width_small, self.layout_configuration.icon_width_small),
            )

            self._dwg.add(
                self._dwg.text(
                    self.translator.get_label(ssb[0].title),
                    insert=(x_3, y_top + 0.5 * self._row_height),
                    font_size=self.layout_configuration.font_size,
                    font_family="Arial",
                    font_weight="normal",
                    font_style="normal",
                    text_anchor="start",
                    dominant_baseline="middle",
                )
            )

            y_top += self.layout_configuration.icon_width_small + self.layout_configuration.small_margin
