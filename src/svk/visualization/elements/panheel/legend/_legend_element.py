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
from svk.data import Label, Color, KnownColors, TimeFrame
from svk.visualization.elements._priority_icon_element import PriorityIconElement
from svk.visualization.elements._text_element import TextElement
from svk.visualization.elements._time_frame_element import TimeFrameElement
from svk.visualization.elements._visual_elements_container import Alignment, VisualElementsContainer
from svk.visualization.elements.panheel.legend._color_table_legend_element import ColorTableLegendElement
from svk.visualization.helpers._color_helper import get_contrast_color, get_color
from svk.visualization.helpers._draw_callout import draw_callout
from svk.visualization.helpers._measuretext import measure_text


class LegendElement(VisualElementsContainer):
    color: Color
    """The color of the group"""
    use_contrast_color: bool = False
    """Indicates whether the title should choose a color with mist contrast or just use black"""

    _color_table_element: ColorTableLegendElement = PrivateAttr()
    _width: float = PrivateAttr()
    _height: float = PrivateAttr()
    _priority_width: float = PrivateAttr()
    _priority_height: float = PrivateAttr()
    _code_explanation_height: float = PrivateAttr()

    _code_explanation_lines: tuple[tuple[str, str, str], ...] = (
        ("Verklaring codes (SP_XX##)", "", ""),
        ("SP", "Vraag gesteld bij sessie met Sluizencomplex Panheel", ""),
        ("XX", "Code die aangeeft wat de herkomst is van de vraag:", ""),
        ("", "C", "Vraag afkomstig uit inventarisatie componenten."),
        ("", "ET", "Vraag afkomstig uit einde technische levenstuur analyse."),
        ("", "EF", "Vraag afkomstig uit einde functionele levenstuur analyse."),
        ("", "A", "Algemeen geldende kennisvraag"),
        ("##", "Volgnummer van de vraag.", ""),
    )

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

        self._code_explanation_height = len(self._code_explanation_lines) * 1.2 * self.layout_configuration.font_size

        # This assumes the code explanation is less wide that the table and priority explanation
        self._width = (
            self.layout_configuration.arrow_depth
            + self.layout_configuration.intermediate_margin
            + self._color_table_element.width
            + self.layout_configuration.intermediate_margin * 2.0
            + self._priority_width
            + self.layout_configuration.intermediate_margin
        )

        self._height = (
            self.layout_configuration.group_header_height
            + self.layout_configuration.intermediate_margin
            + max([self._color_table_element.height, self._priority_height])
            + self.layout_configuration.intermediate_margin
            + self._code_explanation_height
            + self.layout_configuration.intermediate_margin
        )
        return self

    def draw(self, dwg: Drawing, x: float, y: float):
        self._draw_container(dwg=dwg, x=x, y=y)
        _x_left_table = x + self.layout_configuration.arrow_depth + self.layout_configuration.intermediate_margin
        _y_top = y + self.layout_configuration.group_header_height + self.layout_configuration.intermediate_margin
        self._draw_table(
            dwg=dwg,
            x_left=_x_left_table,
            y_top=_y_top,
        )
        self.draw_vertical_separator(
            dwg=dwg,
            x=_x_left_table + self._color_table_element.width + self.layout_configuration.intermediate_margin,
            y=_y_top,
            element_height=max([self._color_table_element.height, self._priority_height]),
            color=self.color,
        )

        self._draw_priority_explanation(
            dwg=dwg,
            x_left=_x_left_table + self._color_table_element.width + 2 * self.layout_configuration.intermediate_margin,
            y_top=_y_top,
        )

        _y_code_explanation = (
            _y_top + max([self._color_table_element.height, self._priority_height]) + self.layout_configuration.intermediate_margin * 2
        )
        self.draw_horizontal_separator(
            dwg=dwg,
            x=_x_left_table,
            y=_y_code_explanation - self.layout_configuration.intermediate_margin,
            element_width=self.width - self.layout_configuration.arrow_depth - self.layout_configuration.intermediate_margin * 2.0,
            color=self.color,
        )
        self._draw_code_explanation(dwg=dwg, x_left=_x_left_table, y_top=_y_code_explanation)

    def _draw_code_explanation(self, dwg: Drawing, x_left: float, y_top: float):
        code_style = dict(font_size=self.layout_configuration.font_size, font_family="Arial", font_wreight="bold")

        text_style = dict(font_size=self.layout_configuration.font_size, font_family="Arial", font_wreight="normal")

        y_current = y_top
        for l in self._code_explanation_lines:
            text = dwg.text("", insert=(x_left, y_current))
            if l[0] is not "":
                text.add(dwg.tspan(l[0], **code_style))
            if l[1] is not "":
                style = text_style if l[0] != "" else code_style
                text.add(dwg.tspan(l[1], dx=[20], **style))
            if l[2] is not "":
                text.add(dwg.tspan(l[2], dx=[40], **text_style))

            dwg.add(text)
            y_current += self.layout_configuration.font_size * 1.2

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
            height_container=self._color_table_element.height,
            width_container=self._color_table_element.width,
            alignment=Alignment.TopLeft,
        )

    def _draw_priority_explanation(self, dwg: Drawing, x_left: float, y_top: float):
        y_current = y_top
        self.draw_element(
            dwg=dwg,
            element=self._high_priority_icon_element,
            x_container=x_left,
            y_container=y_current,
            height_container=max([self._high_priority_icon_element.height, self._high_priority_text_element.height]),
            width_container=self.width,
            alignment=Alignment.MiddleLeft,
        )
        self.draw_element(
            dwg=dwg,
            element=self._high_priority_text_element,
            x_container=x_left + self._high_priority_icon_element.width + self.layout_configuration.small_margin,
            y_container=y_current,
            height_container=max([self._high_priority_icon_element.height, self._high_priority_text_element.height]),
            width_container=self.width,
            alignment=Alignment.MiddleLeft,
        )

        y_current += max([self._high_priority_icon_element.height, self._high_priority_text_element.height])
        self.draw_element(
            dwg=dwg,
            element=self._low_priority_icon_element,
            x_container=x_left,
            y_container=y_current,
            height_container=max([self._high_priority_icon_element.height, self._high_priority_text_element.height]),
            width_container=self.width,
            alignment=Alignment.MiddleLeft,
        )
        self.draw_element(
            dwg=dwg,
            element=self._low_priority_text_element,
            x_container=x_left + self._high_priority_icon_element.width + self.layout_configuration.small_margin,
            y_container=y_current,
            height_container=max([self._high_priority_icon_element.height, self._high_priority_text_element.height]),
            width_container=self.width,
            alignment=Alignment.MiddleLeft,
        )
