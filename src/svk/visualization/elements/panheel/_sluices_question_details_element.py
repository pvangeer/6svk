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
from pydantic import PrivateAttr
from svk.data import SluicesResearchQuestion, Label, Color, IconProvider
from svk.visualization._layout_configuration import LayoutConfiguration
from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.helpers._wrappedtext import wrapped_text, wrapped_lines
from svk.visualization.elements._wrapped_text_element import WrappedTextElement
from svk.visualization.elements._visual_elements_container import VisualElementsContainer, Alignment
from svk.visualization.elements.panheel._sluices_question_priority_details_element import SluicesQuestionPriorityDetailsElement
from svk.visualization.elements._time_frame_element import TimeFrameElement
from svk.visualization.elements._priority_icon_element import PriorityIconElement
from svk.visualization.elements._id_element import IdElement
from svk.visualization.elements._icons_element import IconsElement
from svk.visualization.elements.panheel._sluices_current_research_element import CurrentResearchDetailsElement


class SluicesQuestionDetailsElement(VisualElementsContainer):
    research_question: SluicesResearchQuestion
    """The research question"""
    page_number: int
    color: Color
    first_column_width: float

    _priority_icon_element: PriorityIconElement = PrivateAttr()
    _time_frame_element: TimeFrameElement = PrivateAttr()
    _priority_details_element: SluicesQuestionPriorityDetailsElement = PrivateAttr()
    _current_research_element: CurrentResearchDetailsElement = PrivateAttr()
    _id_element: IdElement = PrivateAttr()

    _h_first_line: float = PrivateAttr()
    _last_line_keywords: list[str] = PrivateAttr()
    _h_last_line: float = PrivateAttr()

    @staticmethod
    def predict_first_column_width(question: SluicesResearchQuestion, layout_configuration: LayoutConfiguration) -> float:
        return max(
            [
                PriorityIconElement.predict_width(layout_configuration),
                IdElement.predict_width(question.id, layout_configuration.font_size),
                TimeFrameElement.predict_width(question.time_frame, layout_configuration=layout_configuration),
            ]
        )

    def initialize(self) -> None:
        self._id_element = self.create(
            IdElement,
            id=self.research_question.id,
            is_link_target=True,
            preferred_width=self.first_column_width,
            page_number=self.page_number,
        )
        self._priority_icon_element = self.create(
            PriorityIconElement,
            priority=self.research_question.priority,
        )

        self._priority_details_element = self.create(
            SluicesQuestionPriorityDetailsElement,
            research_question=self.research_question,
            color=self.color,
        )
        self._ssb_icons_element = self.create(
            IconsElement,
            icons=tuple([IconProvider.create_rws_sluice_icon()]),
        )

        self._time_frame_element = self.create(
            TimeFrameElement,
            time_frame=self.research_question.time_frame,
        )
        self._current_research_element = self.create(
            CurrentResearchDetailsElement,
            research_question=self.research_question,
            color=self.color,
        )
        self._related_question_elements = [
            self.create(
                IdElement,
                id=id,
                is_link=True,
                page_number=self.page_number,
                is_bottom_margin=True,
            )
            for id in self.research_question.reference_ids
        ]

        self._width_first_column = max(
            [self.first_column_width, self._priority_icon_element.width, self._id_element.width, self._time_frame_element.width]
        )

        self._width = self._width_first_column + self._priority_details_element.width + self._current_research_element.width

        self._question_wrapped_text_element = self.create(
            WrappedTextElement,
            text=self.research_question.question,
            max_width=self.width - self._id_element.width - self._ssb_icons_element.width - 2 * self.layout_configuration.small_margin,
        )

        self._h_first_line = max([self._ssb_icons_element.height, self._question_wrapped_text_element.height])

        self._last_line_keywords = wrapped_lines(
            self.translator.get_label(Label.QD_Keywords)
            + ": "
            + (self.research_question.keywords if self.research_question.keywords is not None else "-"),
            self._width
            - self._time_frame_element.width
            - self.layout_configuration.paper_margin * 2.0
            - self.layout_configuration.small_margin * 2,
        )
        self._h_last_line = max(
            [
                (
                    self.layout_configuration.small_margin
                    + self.layout_configuration.font_size * 1.2
                    + self.layout_configuration.small_margin
                    + len(self._last_line_keywords) * 1.2 * self.layout_configuration.font_size
                    + self.layout_configuration.small_margin
                ),
                self._time_frame_element.height,
            ]
        )

    def measure(self) -> None:
        self._height = (
            self._h_first_line
            + max(
                [
                    self._priority_icon_element.height,
                    self._priority_details_element.height,
                    self._current_research_element.height,
                ]
            )
            + self._h_last_line
        )

    def _draw(self, x: float, y: float):
        self._dwg.add(
            self._dwg.rect(
                insert=(x, y),
                size=(self.width, self.height),
                stroke_width=0.5,
                fill=str(self.color),
                fill_opacity=0.3,
                stroke=str(self.color),
            )
        )

        self.draw_first_line(x, y)
        self.draw_horizontal_separator(x, y + self._h_first_line, self.width, self.color)
        self.draw_second_line(x, y + self._h_first_line)
        y_last_line = y + self.height - self._h_last_line
        self.draw_horizontal_separator(x, y_last_line, self.width, self.color)
        self.draw_last_lines(x, y_last_line)

    def draw_first_line(self, x: float, y: float):
        self.draw_element(
            element=self._id_element,
            x_container=x,
            y_container=y,
            width_container=self._width_first_column,
            height_container=self._h_first_line,
            alignment=Alignment.MiddleCenter,
        )
        self.draw_vertical_separator(x + self._width_first_column, y, element_height=self._h_first_line, color=self.color)

        self.draw_element(
            element=self._question_wrapped_text_element,
            x_container=x + self._width_first_column,
            y_container=y,
            width_container=self._question_wrapped_text_element.width,
            height_container=self._h_first_line,
            alignment=Alignment.MiddleLeft,
        )
        self.draw_vertical_separator(x + self.width - self._ssb_icons_element.width, y, element_height=self._h_first_line, color=self.color)
        self.draw_element(
            element=self._ssb_icons_element,
            x_container=x + self.width - self._ssb_icons_element.width,
            y_container=y,
            width_container=self._ssb_icons_element.width,
            height_container=self._h_first_line,
            alignment=Alignment.MiddleCenter,
        )

    def draw_second_line(self, x: float, y: float):
        x_current = x
        height_container = self.height - self._h_first_line - self._h_last_line

        self.draw_element(
            element=self._priority_icon_element,
            x_container=x_current,
            y_container=y,
            width_container=self._width_first_column,
            height_container=height_container,
            alignment=Alignment.MiddleCenter,
        )
        x_current += self._width_first_column
        self.draw_vertical_separator(x_current, y, height_container, self.color)
        self.draw_element(
            element=self._priority_details_element,
            x_container=x_current,
            y_container=y,
            width_container=self._priority_details_element.width,
            height_container=height_container,
            alignment=Alignment.TopLeft,
        )
        x_current += self._priority_details_element.width
        self.draw_vertical_separator(x_current, y, height_container, self.color)
        self.draw_element(
            element=self._current_research_element,
            x_container=x_current,
            y_container=y,
            width_container=self._priority_details_element.width,
            height_container=height_container,
            alignment=Alignment.TopLeft,
        )

    def draw_last_lines(self, x: float, y: float):
        self.draw_element(
            element=self._time_frame_element,
            x_container=x,
            y_container=y,
            width_container=self._width_first_column,
            height_container=self._h_last_line,
            alignment=Alignment.MiddleCenter,
        )

        x_base = x + self._width_first_column

        self.draw_vertical_separator(x=x_base, y=y, element_height=self._h_last_line, color=self.color)

        label = self.translator.get_label(Label.QD_Related_Questions) + ":"
        if len(self._related_question_elements) == 0:
            label += " -"
        self._dwg.add(
            self._dwg.text(
                label,
                insert=(x_base + self.layout_configuration.small_margin, y + self.layout_configuration.small_margin),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )
        x_current = x_base + self.layout_configuration.small_margin + measure_text(label, self.layout_configuration.font_size)[0]
        for related in self._related_question_elements:
            self.draw_element(
                element=related,
                x_container=x_current,
                y_container=y,
                width_container=related.width,
                height_container=related.height,
            )
            x_current += related.width + self.layout_configuration.small_margin

        y_keywords = y + 2 * self.layout_configuration.small_margin + self.layout_configuration.font_size * 1.2
        self._dwg.add(
            wrapped_text(
                dwg=self._dwg,
                lines=self._last_line_keywords,
                insert=(
                    x_base + self.layout_configuration.small_margin,
                    y_keywords,
                ),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                text_anchor="left",
                dominant_baseline="text-before-edge",
            )
        )
