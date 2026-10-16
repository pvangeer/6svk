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
from svk.data import Label, Color, KnownColors
from svk.visualization.elements._visual_elements_container import Alignment, VisualElementsContainer
from svk.visualization.elements.legend._color_table_legend_element import ColorTableLegendElement
from svk.visualization.elements.legend._priority_legend_element import PriorityLegendElement
from svk.visualization.elements.legend._sluices_code_explanation_legend_element import SluicesCodeExplanationLegendElement
from svk.visualization.helpers._color_helper import get_contrast_color
from svk.visualization.helpers._draw_callout import draw_callout


class SluicesLegendElement(VisualElementsContainer):
    color: Color
    """The color of the group"""
    use_contrast_color: bool = False
    """Indicates whether the title should choose a color with mist contrast or just use black"""

    _color_table_legend_element: ColorTableLegendElement = PrivateAttr()
    _priority_legend_element: PriorityLegendElement = PrivateAttr()
    _sluices_code_explanation_legend_element: SluicesCodeExplanationLegendElement = PrivateAttr()
    _content_height: float = PrivateAttr()
    _width: float = PrivateAttr()
    _height: float = PrivateAttr()

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    @model_validator(mode="after")
    def validate(self) -> SluicesLegendElement:
        self._color_table_legend_element = self.create(
            ColorTableLegendElement,
            color=self.color,
            use_rijkswaterstaat_colors=True,
        )
        self._priority_legend_element = self.create(
            PriorityLegendElement,
        )
        self._sluices_code_explanation_legend_element = self.create(
            SluicesCodeExplanationLegendElement,
        )

        self._width = (
            self.layout_configuration.arrow_depth
            + self.layout_configuration.intermediate_margin
            + self._color_table_legend_element.width
            + self.layout_configuration.intermediate_margin * 2.0
            + self._sluices_code_explanation_legend_element.width
            + self.layout_configuration.intermediate_margin * 2.0
            + self._priority_legend_element.width
            + self.layout_configuration.intermediate_margin
        )

        self._content_height = max(
            [
                self._color_table_legend_element.height,
                self._sluices_code_explanation_legend_element.height,
                self._priority_legend_element.height,
            ]
        )
        self._height = (
            self.layout_configuration.group_header_height
            + self.layout_configuration.intermediate_margin
            + self._content_height
            + self.layout_configuration.intermediate_margin
        )
        return self

    def _draw(self, x: float, y: float):
        self._draw_container(x=x, y=y)

        _elements_to_plot = (self._color_table_legend_element, self._sluices_code_explanation_legend_element, self._priority_legend_element)

        _x_left_content = x + self.layout_configuration.arrow_depth + self.layout_configuration.intermediate_margin
        _y_top_content = y + self.layout_configuration.group_header_height + self.layout_configuration.intermediate_margin

        for _element in _elements_to_plot:
            self.draw_element(
                element=_element,
                x_container=_x_left_content,
                y_container=_y_top_content,
                width_container=_element.width,
                height_container=self._content_height,
                alignment=Alignment.MiddleCenter,
            )
            self.draw_vertical_separator(

                x=_x_left_content + _element.width + self.layout_configuration.intermediate_margin,
                y=_y_top_content,
                element_height=self._content_height,
                color=self.color,
            )
            _x_left_content += _element.width + self.layout_configuration.intermediate_margin * 2

    def _draw_container(self, x: float, y: float):
        draw_callout(
            dwg=self._dwg,
            x=x,
            y=y,
            width=self.width,
            height=self.height,
            stroke=KnownColors.GreyAccent,
            fill=KnownColors.White,
            header_fill=KnownColors.GreyAccent,
            stroke_width=1.0,
            arrow_height=30.0,
            arrow_depth=20.0,
            use_gradients=False,
        )
        text_fill = (
            str(get_contrast_color(self.color))
            if self.use_contrast_color or not self.layout_configuration.use_gradients
            else str(KnownColors.Black)
        )
        x_left = x + self.layout_configuration.arrow_depth + self.layout_configuration.intermediate_margin

        self._dwg.add(
            self._dwg.text(
                self.translator.get_label(Label.LegendTitle),
                insert=(
                    x_left,
                    y + self.layout_configuration.group_header_height / 2,
                ),
                font_size=self.layout_configuration.group_title_font_size,
                font_family="Arial",
                font_weight="bold",
                text_anchor="start",
                dominant_baseline="middle",
                fill=text_fill,
            )
        )
