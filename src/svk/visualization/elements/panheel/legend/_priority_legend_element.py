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
from svk.data import Label, Color
from svk.visualization.elements._priority_icon_element import PriorityIconElement
from svk.visualization.elements._text_element import TextElement
from svk.visualization.elements._visual_elements_container import Alignment, VisualElementsContainer
from svk.visualization.elements.panheel.legend._color_table_legend_element import ColorTableLegendElement


class PriorityLegendElement(VisualElementsContainer):
    color: Color
    """The color of the group"""
    use_contrast_color: bool = False
    """Indicates whether the title should choose a color with mist contrast or just use black"""

    _color_table_element: ColorTableLegendElement = PrivateAttr()
    _width: float = PrivateAttr()
    _height: float = PrivateAttr()
    _priority_width: float = PrivateAttr()
    _priority_height: float = PrivateAttr()

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    @model_validator(mode="after")
    def validate(self) -> PriorityLegendElement:
        self._high_priority_icon_element = PriorityIconElement(
            translator=self.translator, layout_configuration=self.layout_configuration, links_register=self.links_register, priority=1
        )
        self._low_priority_icon_element = PriorityIconElement(
            translator=self.translator, layout_configuration=self.layout_configuration, links_register=self.links_register, priority=0
        )
        self._high_priority_text_element = TextElement(
            translator=self.translator,
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            text=self.translator.get_label(Label.LegendHighPriority),
        )
        self._low_priority_text_element = TextElement(
            translator=self.translator,
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            text=self.translator.get_label(Label.LegendLowPriority),
        )

        self._priority_width = (
            max([self._high_priority_icon_element.width, self._low_priority_icon_element.width])
            + self.layout_configuration.small_margin
            + max([self._high_priority_text_element.width, self._low_priority_text_element.width])
            + 2 * self.layout_configuration.small_margin
        )
        self._priority_height = max([self._high_priority_icon_element.height, self._high_priority_text_element.height]) + max(
            [self._low_priority_icon_element.height, self._low_priority_text_element.height]
        )

        self._width = self._priority_width
        self._height = self._priority_height

        return self

    def draw(self, dwg: Drawing, x: float, y: float):
        y_current = y
        self.draw_element(
            dwg=dwg,
            element=self._high_priority_icon_element,
            x_container=x,
            y_container=y_current,
            height_container=max([self._high_priority_icon_element.height, self._high_priority_text_element.height]),
            width_container=self.width,
            alignment=Alignment.MiddleLeft,
        )
        self.draw_element(
            dwg=dwg,
            element=self._high_priority_text_element,
            x_container=x + self._high_priority_icon_element.width + self.layout_configuration.small_margin,
            y_container=y_current,
            height_container=max([self._high_priority_icon_element.height, self._high_priority_text_element.height]),
            width_container=self.width,
            alignment=Alignment.MiddleLeft,
        )

        y_current += max([self._high_priority_icon_element.height, self._high_priority_text_element.height])
        self.draw_element(
            dwg=dwg,
            element=self._low_priority_icon_element,
            x_container=x,
            y_container=y_current,
            height_container=max([self._high_priority_icon_element.height, self._high_priority_text_element.height]),
            width_container=self.width,
            alignment=Alignment.MiddleLeft,
        )
        self.draw_element(
            dwg=dwg,
            element=self._low_priority_text_element,
            x_container=x + self._high_priority_icon_element.width + self.layout_configuration.small_margin,
            y_container=y_current,
            height_container=max([self._high_priority_icon_element.height, self._high_priority_text_element.height]),
            width_container=self.width,
            alignment=Alignment.MiddleLeft,
        )
