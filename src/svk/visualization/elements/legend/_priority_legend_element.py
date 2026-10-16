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
from svk.data import Label
from svk.visualization.elements._priority_icon_element import PriorityIconElement
from svk.visualization.elements._text_element import TextElement
from svk.visualization.elements._visual_elements_container import Alignment, VisualElementsContainer
from svk.visualization.elements.legend._color_table_legend_element import ColorTableLegendElement


class PriorityLegendElement(VisualElementsContainer):
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
        self._high_priority_icon_element = self.create(
            PriorityIconElement,
            priority=1
        )
        self._low_priority_icon_element = self.create(
            PriorityIconElement,
            priority=0
        )
        self._high_priority_text_element = self.create(
            TextElement,
            text=self.translator.get_label(Label.LegendHighPriority),
        )
        self._low_priority_text_element = self.create(
            TextElement,
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

    def _draw(self, x: float, y: float):
        y_current = y
        self.draw_element(
            element=self._high_priority_icon_element,
            x_container=x,
            y_container=y_current,
            height_container=max([self._high_priority_icon_element.height, self._high_priority_text_element.height]),
            width_container=self.width,
            alignment=Alignment.MiddleLeft,
        )
        self.draw_element(
            element=self._high_priority_text_element,
            x_container=x + self._high_priority_icon_element.width + self.layout_configuration.small_margin,
            y_container=y_current,
            height_container=max([self._high_priority_icon_element.height, self._high_priority_text_element.height]),
            width_container=self.width,
            alignment=Alignment.MiddleLeft,
        )

        y_current += max([self._high_priority_icon_element.height, self._high_priority_text_element.height])
        self.draw_element(
            element=self._low_priority_icon_element,
            x_container=x,
            y_container=y_current,
            height_container=max([self._high_priority_icon_element.height, self._high_priority_text_element.height]),
            width_container=self.width,
            alignment=Alignment.MiddleLeft,
        )
        self.draw_element(
            element=self._low_priority_text_element,
            x_container=x + self._high_priority_icon_element.width + self.layout_configuration.small_margin,
            y_container=y_current,
            height_container=max([self._high_priority_icon_element.height, self._high_priority_text_element.height]),
            width_container=self.width,
            alignment=Alignment.MiddleLeft,
        )
