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
from svk.data import Label, Color, KnownColors
from svk.visualization.elements._visual_elements_container import Alignment, VisualElementsContainer
from svk.visualization.elements.panheel.legend._color_table_legend_element import ColorTableLegendElement
from svk.visualization.elements.panheel.legend._priority_legend_element import PriorityLegendElement
from svk.visualization.elements.panheel.legend._code_explanation_legend_element import CodeExplanationLegendElement
from svk.visualization.helpers._color_helper import get_contrast_color
from svk.visualization.helpers._draw_callout import draw_callout


class LegendElement(VisualElementsContainer):
    color: Color
    """The color of the group"""
    use_contrast_color: bool = False
    """Indicates whether the title should choose a color with mist contrast or just use black"""

    _color_table_element: ColorTableLegendElement = PrivateAttr()
    _priority_element: PriorityLegendElement = PrivateAttr()
    _code_explanation_element: CodeExplanationLegendElement = PrivateAttr()
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
    def validate(self) -> LegendElement:
        self._color_table_element = ColorTableLegendElement(
            translator=self.translator, layout_configuration=self.layout_configuration, links_register=self.links_register, color=self.color
        )
        self._priority_element = PriorityLegendElement(
            translator=self.translator, layout_configuration=self.layout_configuration, links_register=self.links_register, color=self.color
        )
        self._code_explanation_element = CodeExplanationLegendElement(
            translator=self.translator, layout_configuration=self.layout_configuration, links_register=self.links_register, color=self.color
        )

        self._width = (
            self.layout_configuration.arrow_depth
            + self.layout_configuration.intermediate_margin
            + self._color_table_element.width
            + self.layout_configuration.intermediate_margin * 2.0
            + self._code_explanation_element.width
            + self.layout_configuration.intermediate_margin * 2.0
            + self._priority_element.width
            + self.layout_configuration.intermediate_margin
        )

        self._content_height = max([self._color_table_element.height, self._code_explanation_element.height, self._priority_element.height])
        self._height = (
            self.layout_configuration.group_header_height
            + self.layout_configuration.intermediate_margin
            + self._content_height
            + self.layout_configuration.intermediate_margin
        )
        return self

    def draw(self, dwg: Drawing, x: float, y: float):
        self._draw_container(dwg=dwg, x=x, y=y)
        _x_left_content = x + self.layout_configuration.arrow_depth + self.layout_configuration.intermediate_margin
        _y_top_content = y + self.layout_configuration.group_header_height + self.layout_configuration.intermediate_margin
        self._draw_table(
            dwg=dwg,
            x_left=_x_left_content,
            y_top=_y_top_content,
        )
        self.draw_vertical_separator(
            dwg=dwg,
            x=_x_left_content + self._color_table_element.width + self.layout_configuration.intermediate_margin,
            y=_y_top_content,
            element_height=self._content_height,
            color=self.color,
        )
        _x_left_code_explanation = _x_left_content + self._color_table_element.width + 2 * self.layout_configuration.intermediate_margin
        self._draw_code_explanation(dwg=dwg, x_left=_x_left_code_explanation, y_top=_y_top_content)
        self.draw_vertical_separator(
            dwg=dwg,
            x=_x_left_code_explanation + self._code_explanation_element.width + self.layout_configuration.intermediate_margin,
            y=_y_top_content,
            element_height=self._content_height,
            color=self.color,
        )
        _x_left_priority = (
            _x_left_code_explanation + self._code_explanation_element.width + 2 * self.layout_configuration.intermediate_margin
        )
        self._draw_priority_explanation(
            dwg=dwg,
            x_left=_x_left_priority,
            y_top=_y_top_content,
        )

    def _draw_priority_explanation(self, dwg: Drawing, x_left: float, y_top: float):
        self.draw_element(
            dwg=dwg,
            element=self._priority_element,
            x_container=x_left,
            y_container=y_top,
            height_container=self._content_height,
            width_container=self._priority_element.width,
            alignment=Alignment.MiddleCenter,
        )

    def _draw_code_explanation(self, dwg: Drawing, x_left: float, y_top: float):
        self.draw_element(
            dwg=dwg,
            element=self._code_explanation_element,
            x_container=x_left,
            y_container=y_top,
            height_container=self._content_height,
            width_container=self._code_explanation_element.width,
            alignment=Alignment.MiddleCenter,
        )

    def _draw_container(self, dwg: Drawing, x: float, y: float):
        draw_callout(
            dwg=dwg,
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

        dwg.add(
            dwg.text(
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

    def _draw_table(self, dwg: Drawing, x_left: float, y_top: float):
        self.draw_element(
            dwg=dwg,
            element=self._color_table_element,
            x_container=x_left,
            y_container=y_top,
            height_container=self._content_height,
            width_container=self._color_table_element.width,
            alignment=Alignment.MiddleCenter,
        )
