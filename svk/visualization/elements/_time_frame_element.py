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
from svk.data import TimeFrame
from svk.visualization.elements._visual_elements_container import VisualElementsContainer
from svk.visualization.helpers._draw_scaled_icon import Symbol, Path, accent_fill


class TimeFrameElement(VisualElementsContainer):
    """A container for the storm surge barrier icons."""

    time_frame: TimeFrame
    """The storm surge barriers to display icons for."""

    _height: float = PrivateAttr()
    _width: float = PrivateAttr()

    @model_validator(mode="after")
    def validate(self) -> TimeFrameElement:

        self._width = (
            self.layout_configuration.small_margin + self.layout_configuration.icon_width_small + self.layout_configuration.small_margin
        )
        self._height = (
            self.layout_configuration.small_margin + self.layout_configuration.icon_width_small + self.layout_configuration.small_margin
        )
        return self

    @property
    def height(self) -> float:
        return self._height

    @property
    def width(self) -> float:
        return self._width

    def draw(self, dwg: Drawing, x: float, y: float):
        time_frame_ico = Symbol(id=self.time_frame.name)

        match self.time_frame:
            case TimeFrame.Now:
                time_frame_ico.objects = [
                    Path(
                        d="m 52.550102,189.38019 153.669208,-0.19083 0.1952,72.93908 m 47.44872,-40.78067 -46.99687,40.47311 m -45.43164,-40.73769 44.67828,41.15982"
                    ),
                ]
            case TimeFrame.NearFuture:
                time_frame_ico.objects = [
                    Path(
                        d="m 58.082886,173.69718 179.530904,0.30091 m -40.78067,-47.44872 40.47311,46.99687 m -40.73769,45.43164 41.15982,-44.67828"
                    ),
                ]
            case TimeFrame.Future:
                time_frame_ico.objects = [
                    Path(
                        d="M 34.048204,170.95036 C 95.440663,82.251406 178.95804,105.79218 237.61379,173.99809 m 0.42164,-42.29843 -0.7292,41.84658 m -44.17122,0.45245 44.59335,0.30091"
                    ),
                    Path(d="M 67.960734,174 H 85.128362", stroke_width=10, stroke=accent_fill),
                    Path(d="m 112.3865,174 h 17.16763", stroke_width=10, stroke=accent_fill),
                    Path(d="m 154.78043,174 h 17.16763", stroke_width=10, stroke=accent_fill),
                ]

        x_icon_current = x + self.layout_configuration.small_margin
        y_icon_current = y + self.layout_configuration.small_margin

        time_frame_ico.add_to_dwg(
            dwg=dwg,
            insert=(
                x_icon_current,
                y_icon_current,
            ),
            size=(self.layout_configuration.icon_width_small, self.layout_configuration.icon_width_small),
        )
