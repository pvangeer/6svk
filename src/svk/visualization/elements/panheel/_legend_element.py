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
from svk.visualization.helpers._color_helper import get_contrast_color
from svk.visualization.helpers._draw_callout import draw_callout
from svk.visualization.helpers import _color_helper as colorhelper


class LegendElement(VisualElementsContainer):
    color: Color
    """The color of the group"""
    use_contrast_color: bool = False
    """Indicates whether the title should choose a color with mist contrast or just use black"""

    _width: float = PrivateAttr()
    _height: float = PrivateAttr()
    _maintenance_text_element: TextElement = PrivateAttr()
    _requirements_text_element: TextElement = PrivateAttr()
    _operational_text_element: TextElement = PrivateAttr()
    _column_width: float = PrivateAttr()
    _row_height: float = PrivateAttr()
    _now_icon_element: TimeFrameElement = PrivateAttr()
    _near_future_icon_element: TimeFrameElement = PrivateAttr()
    _future_icon_element: TimeFrameElement = PrivateAttr()

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    @model_validator(mode="after")
    def validate(self) -> LegendElement:
        self._now_icon_element = TimeFrameElement(
            translator=self.translator,
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            time_frame=TimeFrame.Now,
        )
        self._near_future_icon_element = TimeFrameElement(
            translator=self.translator,
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            time_frame=TimeFrame.NearFuture,
        )
        self._future_icon_element = TimeFrameElement(
            translator=self.translator,
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            time_frame=TimeFrame.Future,
        )
        self._maintenance_text_element = TextElement(
            translator=self.translator,
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            text=self.translator.get_label(Label.RLG_Maintenance),
        )
        self._requirements_text_element = TextElement(
            translator=self.translator,
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            text=self.translator.get_label(Label.RLG_Requirements),
        )
        self._operational_text_element = TextElement(
            translator=self.translator,
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            text=self.translator.get_label(Label.RLG_Operational),
        )
        self._heigh_priority_icon_element = PriorityIconElement(
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

        priority_width = (
            max([self._heigh_priority_icon_element.width, self._low_priority_icon_element.width])
            + self.layout_configuration.small_margin
            + max([self._high_priority_text_element.width, self._low_priority_text_element.width])
            + 2 * self.layout_configuration.small_margin
        )
        priority_height = max([self._heigh_priority_icon_element.height, self._high_priority_text_element.height]) + max(
            [self._low_priority_icon_element.height, self._low_priority_text_element.height]
        )

        self._column_width = max(
            [
                self._now_icon_element.width,
                self._near_future_icon_element.width,
                self._future_icon_element.width,
            ]
        )
        self._first_column_width = (
            max(
                [
                    self._requirements_text_element.width,
                    self._maintenance_text_element.width,
                    self._operational_text_element.width,
                ]
            )
            + 2 * self.layout_configuration.small_margin
        )
        self._first_row_height = (
            max(
                [
                    self.layout_configuration.small_margin,
                    self._now_icon_element.height,
                    self._near_future_icon_element.height,
                    self._future_icon_element.height,
                ]
            )
            + 2 * self.layout_configuration.small_margin
        )

        self._width = max(
            [
                priority_width,
                (
                    self.layout_configuration.arrow_depth
                    + self.layout_configuration.intermediate_margin
                    + self._first_column_width
                    + self._column_width * 3
                    + self.layout_configuration.small_margin * 2
                    + self.layout_configuration.intermediate_margin
                ),
            ]
        )
        self._row_height = (
            max([self._requirements_text_element.height, self._maintenance_text_element.height, self._operational_text_element.height])
            + 2 * self.layout_configuration.small_margin
        )
        self._height = (
            self.layout_configuration.group_header_height
            + self.layout_configuration.intermediate_margin
            + self._first_row_height
            + 3 * self._row_height
            + self.layout_configuration.intermediate_margin
            + priority_height
            + self.layout_configuration.intermediate_margin
        )
        return self

    def draw(self, dwg: Drawing, x: float, y: float):
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
        y_r1 = y + self.layout_configuration.group_header_height + self.layout_configuration.intermediate_margin + self._first_row_height

        self.draw_horizontal_separator(
            dwg=dwg,
            x=x_left,
            y=y_r1,
            element_width=self._first_column_width + 3 * self._column_width,
            color=self.color,
        )
        self._draw_research_line_group_element(
            dwg=dwg,
            element=self._maintenance_text_element,
            x_container=x_left + self.layout_configuration.small_margin,
            y_container=y_r1,
        )
        self.draw_horizontal_separator(
            dwg=dwg,
            x=x_left,
            y=y_r1 + self._row_height,
            element_width=self._first_column_width + 3 * self._column_width,
            color=self.color,
        )

        y_r2 = y_r1 + self._row_height
        self._draw_research_line_group_element(
            dwg=dwg,
            element=self._requirements_text_element,
            x_container=x_left + self.layout_configuration.small_margin,
            y_container=y_r2,
        )
        self.draw_horizontal_separator(
            dwg=dwg,
            x=x_left,
            y=y_r2 + self._row_height,
            element_width=self._first_column_width + 3 * self._column_width,
            color=self.color,
        )

        y_r3 = y_r2 + self._row_height
        self._draw_research_line_group_element(
            dwg=dwg,
            element=self._operational_text_element,
            x_container=x_left + self.layout_configuration.small_margin,
            y_container=y_r3,
        )
        self.draw_horizontal_separator(
            dwg=dwg,
            x=x_left,
            y=y_r3 + self._row_height,
            element_width=self._first_column_width + 3 * self._column_width,
            color=self.color,
        )

        x_c1 = x_left + self._first_column_width
        y_top = y + self.layout_configuration.group_header_height + self.layout_configuration.intermediate_margin
        self.draw_vertical_separator(dwg=dwg, x=x_c1, y=y_top, element_height=self._first_row_height, color=self.color)
        self.draw_time_frame_element(dwg=dwg, element=self._now_icon_element, x_container=x_c1, y_container=y_top)

        x_c2 = x_c1 + self._column_width
        self.draw_vertical_separator(dwg=dwg, x=x_c2, y=y_top, element_height=self._first_row_height, color=self.color)
        self.draw_time_frame_element(dwg=dwg, element=self._near_future_icon_element, x_container=x_c2, y_container=y_top)

        x_c3 = x_c2 + self._column_width
        self.draw_vertical_separator(dwg=dwg, x=x_c3, y=y_top, element_height=self._first_row_height, color=self.color)
        self.draw_time_frame_element(dwg=dwg, element=self._future_icon_element, x_container=x_c3, y_container=y_top)

        self.draw_vertical_separator(dwg=dwg, x=x_c3 + self._column_width, y=y_top, element_height=self._first_row_height, color=self.color)

        for i_row, y_r in enumerate([y_r1, y_r2, y_r3]):
            self.draw_vertical_separator(dwg=dwg, x=x_c3 + self._column_width, y=y_r, element_height=self._row_height, color=self.color)
            for i_time_frame, x_c in enumerate([x_c1, x_c2, x_c3]):
                self.draw_vertical_separator(dwg=dwg, x=x_c, y=y_r, element_height=self._row_height, color=self.color)
                dwg.add(
                    dwg.rect(
                        insert=(x_c + self.layout_configuration.small_margin, y_r + self.layout_configuration.small_margin),
                        size=(
                            self._column_width - 2 * self.layout_configuration.small_margin,
                            self._row_height - 2 * self.layout_configuration.small_margin,
                        ),
                        fill=self._get_color(i_time_frame, i_row),
                    )
                )

        y_current = y_r3 + self._row_height + self.layout_configuration.intermediate_margin
        self.draw_element(
            dwg=dwg,
            element=self._heigh_priority_icon_element,
            x_container=x_left,
            y_container=y_current,
            height_container=max([self._heigh_priority_icon_element.height, self._high_priority_text_element.height]),
            width_container=self.width,
            alignment=Alignment.MiddleLeft,
        )
        self.draw_element(
            dwg=dwg,
            element=self._high_priority_text_element,
            x_container=x_left + self._heigh_priority_icon_element.width + self.layout_configuration.small_margin,
            y_container=y_current,
            height_container=max([self._heigh_priority_icon_element.height, self._high_priority_text_element.height]),
            width_container=self.width,
            alignment=Alignment.MiddleLeft,
        )

        y_current += max([self._heigh_priority_icon_element.height, self._high_priority_text_element.height])
        self.draw_element(
            dwg=dwg,
            element=self._low_priority_icon_element,
            x_container=x_left,
            y_container=y_current,
            height_container=max([self._heigh_priority_icon_element.height, self._high_priority_text_element.height]),
            width_container=self.width,
            alignment=Alignment.MiddleLeft,
        )
        self.draw_element(
            dwg=dwg,
            element=self._low_priority_text_element,
            x_container=x_left + self._heigh_priority_icon_element.width + self.layout_configuration.small_margin,
            y_container=y_current,
            height_container=max([self._heigh_priority_icon_element.height, self._high_priority_text_element.height]),
            width_container=self.width,
            alignment=Alignment.MiddleLeft,
        )

    def draw_time_frame_element(self, dwg: Drawing, element: TimeFrameElement, x_container: float, y_container: float):
        self.draw_element(
            dwg=dwg,
            element=element,
            x_container=x_container,
            y_container=y_container,
            width_container=self._column_width,
            height_container=self._first_row_height,
            alignment=Alignment.MiddleCenter,
        )

    def _draw_research_line_group_element(self, dwg: Drawing, element: TextElement, x_container: float, y_container: float):
        self.draw_element(
            dwg=dwg,
            element=element,
            x_container=x_container,
            y_container=y_container,
            width_container=self._first_column_width - 2 * self.layout_configuration.small_margin,
            height_container=self._row_height,
            alignment=Alignment.MiddleRight,
        )

    def _get_color(self, i_time_frame: int, i_row: int) -> Color:
        match i_time_frame:
            case 0:
                current_time_frame = TimeFrame.Now
            case 1:
                current_time_frame = TimeFrame.NearFuture
            case 2:
                current_time_frame = TimeFrame.Future
            case _:
                current_time_frame = TimeFrame.Unknown

        return colorhelper.get_color(self.layout_configuration, current_time_frame, research_line_group=i_row + 1)
