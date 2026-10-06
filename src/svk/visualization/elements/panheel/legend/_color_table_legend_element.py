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
from svk.data import Label, Color, TimeFrame
from svk.visualization.elements._text_element import TextElement
from svk.visualization.elements._time_frame_element import TimeFrameElement
from svk.visualization.elements._visual_elements_container import Alignment, VisualElementsContainer
from svk.visualization.helpers._color_helper import get_color


class ColorTableLegendElement(VisualElementsContainer):
    color: Color
    """The color of the group"""
    use_contrast_color: bool = False
    """Indicates whether the title should choose a color with mist contrast or just use black"""

    _width: float = PrivateAttr()
    _height: float = PrivateAttr()
    _maintenance_text_element: TextElement = PrivateAttr()
    _requirements_text_element: TextElement = PrivateAttr()
    _operational_text_element: TextElement = PrivateAttr()
    _table_column_width: float = PrivateAttr()
    _row_height: float = PrivateAttr()
    _table_width: float = PrivateAttr()
    _table_height: float = PrivateAttr()
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
    def validate(self) -> ColorTableLegendElement:
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

        self._table_column_width = max(
            [
                self._now_icon_element.width,
                self._near_future_icon_element.width,
                self._future_icon_element.width,
            ]
        )
        self._table_first_column_width = (
            max(
                [
                    self._requirements_text_element.width,
                    self._maintenance_text_element.width,
                    self._operational_text_element.width,
                ]
            )
            + 2 * self.layout_configuration.small_margin
        )
        self._table_first_row_height = (
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

        self._table_width = (
            +self._table_first_column_width
            + self._table_column_width * 3
            + self.layout_configuration.small_margin * 2
            + self.layout_configuration.intermediate_margin
        )

        self._width = self._table_width

        self._row_height = (
            max([self._requirements_text_element.height, self._maintenance_text_element.height, self._operational_text_element.height])
            + 2 * self.layout_configuration.small_margin
        )
        self._table_height = self._table_first_row_height + 3 * self._row_height
        self._height = self._table_height
        return self

    def draw(self, dwg: Drawing, x: float, y: float):
        y_r1 = y + self._table_first_row_height
        self.draw_horizontal_separator(
            dwg=dwg,
            x=x,
            y=y_r1,
            element_width=self._table_first_column_width + 3 * self._table_column_width,
            color=self.color,
        )
        self._draw_research_line_group_element(
            dwg=dwg,
            element=self._maintenance_text_element,
            x_container=x + self.layout_configuration.small_margin,
            y_container=y_r1,
        )
        self.draw_horizontal_separator(
            dwg=dwg,
            x=x,
            y=y_r1 + self._row_height,
            element_width=self._table_first_column_width + 3 * self._table_column_width,
            color=self.color,
        )

        y_r2 = y_r1 + self._row_height
        self._draw_research_line_group_element(
            dwg=dwg,
            element=self._requirements_text_element,
            x_container=x + self.layout_configuration.small_margin,
            y_container=y_r2,
        )
        self.draw_horizontal_separator(
            dwg=dwg,
            x=x,
            y=y_r2 + self._row_height,
            element_width=self._table_first_column_width + 3 * self._table_column_width,
            color=self.color,
        )

        y_r3 = y_r2 + self._row_height
        self._draw_research_line_group_element(
            dwg=dwg,
            element=self._operational_text_element,
            x_container=x + self.layout_configuration.small_margin,
            y_container=y_r3,
        )

        x_c1 = x + self._table_first_column_width
        self.draw_vertical_separator(dwg=dwg, x=x_c1, y=y, element_height=self._table_first_row_height, color=self.color)
        self._draw_time_frame_element(dwg=dwg, element=self._now_icon_element, x_container=x_c1, y_container=y)

        x_c2 = x_c1 + self._table_column_width
        self.draw_vertical_separator(dwg=dwg, x=x_c2, y=y, element_height=self._table_first_row_height, color=self.color)
        self._draw_time_frame_element(dwg=dwg, element=self._near_future_icon_element, x_container=x_c2, y_container=y)

        x_c3 = x_c2 + self._table_column_width
        self.draw_vertical_separator(dwg=dwg, x=x_c3, y=y, element_height=self._table_first_row_height, color=self.color)
        self._draw_time_frame_element(dwg=dwg, element=self._future_icon_element, x_container=x_c3, y_container=y)

        for i_row, y_r in enumerate([y_r1, y_r2, y_r3]):
            for i_time_frame, x_c in enumerate([x_c1, x_c2, x_c3]):
                self.draw_vertical_separator(dwg=dwg, x=x_c, y=y_r, element_height=self._row_height, color=self.color)
                dwg.add(
                    dwg.rect(
                        insert=(x_c + self.layout_configuration.small_margin, y_r + self.layout_configuration.small_margin),
                        size=(
                            self._table_column_width - 2 * self.layout_configuration.small_margin,
                            self._row_height - 2 * self.layout_configuration.small_margin,
                        ),
                        fill=self._get_color(i_time_frame, i_row),
                    )
                )

    def _draw_time_frame_element(self, dwg: Drawing, element: TimeFrameElement, x_container: float, y_container: float):
        self.draw_element(
            dwg=dwg,
            element=element,
            x_container=x_container,
            y_container=y_container,
            width_container=self._table_column_width,
            height_container=self._table_first_row_height,
            alignment=Alignment.MiddleCenter,
        )

    def _draw_research_line_group_element(self, dwg: Drawing, element: TextElement, x_container: float, y_container: float):
        self.draw_element(
            dwg=dwg,
            element=element,
            x_container=x_container,
            y_container=y_container,
            width_container=self._table_first_column_width - 2 * self.layout_configuration.small_margin,
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

        return get_color(self.layout_configuration, current_time_frame, research_line_group=i_row + 1)
