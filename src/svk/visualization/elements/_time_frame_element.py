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
from svk.data import TimeFrame, IconProvider
from svk.visualization.elements._visual_elements_container import VisualElementsContainer
from svk.visualization.helpers._draw_scaled_icon import draw_scaled_icon
from svk.visualization.helpers._calendar_helper import get_time_frame_string
from svk.visualization.helpers._measuretext import measure_text


class TimeFrameElement(VisualElementsContainer):
    """A container for the storm surge barrier icons."""

    time_frame: TimeFrame
    """The storm surge barriers to display icons for."""

    _height: float = PrivateAttr()
    _width: float = PrivateAttr()

    @model_validator(mode="after")
    def validate(self) -> TimeFrameElement:

        _text_width = measure_text(get_time_frame_string(self.time_frame), self.layout_configuration.font_size)[0]
        self._width = (
            self.layout_configuration.small_margin
            + max([self.layout_configuration.icon_width_small, _text_width])
            + self.layout_configuration.small_margin
        )
        self._height = (
            self.layout_configuration.small_margin
            + self.layout_configuration.icon_width_small
            + self.layout_configuration.font_size * 1.2
            + self.layout_configuration.small_margin
        )
        return self

    @property
    def height(self) -> float:
        return self._height

    @property
    def width(self) -> float:
        return self._width

    def draw(self, dwg: Drawing, x: float, y: float):
        icon = IconProvider.create_time_frame_icon(self.time_frame)
        if icon is None:
            raise ValueError("IconProvider could not construct an icon for this time frame. None will be drawn.")

        draw_scaled_icon(
            dwg=dwg,
            icon=icon,
            insert=(
                x + self.width / 2.0 - self.layout_configuration.icon_width_small / 2.0,
                y + self.layout_configuration.small_margin,
            ),
            size=(self.layout_configuration.icon_width_small, self.layout_configuration.icon_width_small),
        )
        _time_frame_text = get_time_frame_string(self.time_frame)
        dwg.add(
            dwg.text(
                _time_frame_text,
                insert=(x + self.width / 2.0, y + self.layout_configuration.small_margin + self.layout_configuration.icon_width_small),
                font_size=self.layout_configuration.font_size,
                text_anchor="middle",
                dominant_baseline="hanging",
                fill="black",
            )
        )
