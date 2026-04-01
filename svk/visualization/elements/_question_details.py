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
from svk.data import ResearchQuestion, Label
from svgwrite import Drawing
from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.helpers._wrappedtext import wrapped_text, wrapped_lines
from svk.visualization.helpers._greyfraction import color_toward_grey
from svk.visualization.elements._wrapped_text_element import WrappedTextElement
from svk.visualization.elements._visual_elements_container import VisualElementsContainer, Alignment
from svk.visualization.elements._question_organisation_details_element import QuestionOrganisationDetailsElement
from svk.visualization.elements._question_priority_details_element import QuestionPriorityDetailsElement
from svk.visualization.elements._priority_icon_element import PriorityIconElement
from svk.visualization.elements._id_element import IdElement
from svk.visualization.elements._question_related_details_element import QuestionRelatedDetailsElement
from svk.visualization.helpers._draw_scaled_icon import draw_scaled_icon


class QuestionDetailsElement(VisualElementsContainer):
    research_question: ResearchQuestion
    """The research question"""
    page_number: int

    _height: float = PrivateAttr()
    _width: float = PrivateAttr()

    _priority_icon_element: PriorityIconElement = PrivateAttr()
    _question_explanation_element: WrappedTextElement = PrivateAttr()
    _priority_details_element: QuestionPriorityDetailsElement = PrivateAttr()
    _organisation_details_element: QuestionOrganisationDetailsElement = PrivateAttr()
    _related_element: QuestionRelatedDetailsElement = PrivateAttr()
    _id_element: IdElement = PrivateAttr()

    _question_lines: list[str] = PrivateAttr()
    _h_first_line: float = PrivateAttr()
    _last_line_keywords: list[str] = PrivateAttr()
    _h_last_line: float = PrivateAttr()

    @property
    def height(self) -> float:
        return self._height

    @property
    def width(self) -> float:
        return self._width

    @model_validator(mode="after")
    def validate(self):
        self._priority_icon_element = PriorityIconElement(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            priority=self.research_question.priority,
        )
        self._question_explanation_element = WrappedTextElement(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            text=self.research_question.explanation if self.research_question.explanation is not None else "-",
            max_width=self.layout_configuration.question_explanation_width,
        )
        self._priority_details_element = QuestionPriorityDetailsElement(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            research_question=self.research_question,
            color=self._color,
        )
        self._organisation_details_element = QuestionOrganisationDetailsElement(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            research_question=self.research_question,
            color=self._color,
            page_number=self.page_number,
        )
        self._related_element = QuestionRelatedDetailsElement(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            research_question=self.research_question,
            color=self._color,
            page_number=self.page_number,
        )
        self._id_element = IdElement(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            id=self.research_question.id,
            is_link_target=True,
            page_number=self.page_number,
        )

        self._width = (
            max([self._priority_icon_element.width, self._id_element.width])
            + self._question_explanation_element.width
            + self._priority_details_element.width
            + self._organisation_details_element.width
            + self._related_element.width
        )

        self._question_lines = wrapped_lines(
            self.research_question.question,
            self.width - self._id_element.width - 2 * self.layout_configuration.small_margin,
            self.layout_configuration.font_size,
        )

        self._h_first_line = (
            self.layout_configuration.small_margin
            + self.layout_configuration.font_size * len(self._question_lines) * 1.2
            + self.layout_configuration.small_margin
        )

        self._last_line_keywords = wrapped_lines(
            self.translator.get_label(Label.QD_Keywords)
            + ": "
            + (self.research_question.keywords if self.research_question.keywords is not "" else ""),
            self.layout_configuration.details_page_width
            - self.layout_configuration.paper_margin * 2.0
            - self.layout_configuration.small_margin * 2,
        )
        self._h_last_line = (
            self.layout_configuration.small_margin
            + len(self._last_line_keywords) * 1.2 * self.layout_configuration.font_size
            + self.layout_configuration.small_margin
        )

        self._height = (
            self._h_first_line
            + max(
                [
                    self._priority_icon_element.height,
                    self._question_explanation_element.height,
                    self._priority_details_element.height,
                    self._organisation_details_element.height,
                    self._related_element.height,
                ]
            )
            + self._h_last_line
        )

        return self

    @property
    def _color(self):
        research_line = self.research_question.research_line_primary
        return (
            color_toward_grey(
                research_line.base_color,
                self.research_question.time_frame.grey_fraction,
            )
            if research_line is not None
            else "rgb(120,120,120)"
        )

    def draw(self, dwg: Drawing, x: float, y: float):
        dwg.add(
            dwg.rect(
                insert=(x, y),
                size=(self.width, self.height),
                stroke_width=0.5,
                fill=self._color,
                fill_opacity=0.3,
                stroke=self._color,
            )
        )

        self.draw_first_line(dwg, x, y)
        self.draw_horizontal_separator(dwg, x, y + self._h_first_line, self.width, self._color)
        self.draw_second_line(dwg, x, y + self._h_first_line)
        y_last_line = y + self.height - self._h_last_line
        self.draw_horizontal_separator(dwg, x, y_last_line, self.width, self._color)
        self.draw_last_lines(dwg, x, y_last_line)

    def draw_first_line(self, dwg: Drawing, x: float, y: float):
        width_first_column = max([self._id_element.width, self._priority_icon_element.width])
        self.draw_element(
            dwg=dwg,
            element=self._id_element,
            x_container=x,
            y_container=y,
            width_container=width_first_column,
            height_container=self._h_first_line,
            alignment=Alignment.MiddleCenter,
        )
        self.draw_vertical_separator(dwg, x + width_first_column, y, element_height=self._h_first_line, color=self._color)
        # TODO: Use WrappedTextElement
        dwg.add(
            wrapped_text(
                dwg,
                self._question_lines,
                insert=(x + width_first_column + self.layout_configuration.small_margin, y + self.layout_configuration.small_margin),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_style="italic",
                font_weight="normal",
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )

    def draw_second_line(self, dwg: Drawing, x: float, y: float):
        x_current = x
        height_container = self.height - self._h_first_line - self._h_last_line
        width_first_column = max([self._priority_icon_element.width, self._id_element.width])
        self.draw_element(
            dwg=dwg,
            element=self._priority_icon_element,
            x_container=x_current,
            y_container=y,
            width_container=width_first_column,
            height_container=height_container,
            alignment=Alignment.MiddleCenter,
        )
        x_current += width_first_column
        self.draw_vertical_separator(dwg, x_current, y, height_container, self._color)
        self.draw_element(
            dwg=dwg,
            element=self._question_explanation_element,
            x_container=x_current,
            y_container=y,
            width_container=self._question_explanation_element.width,
            height_container=height_container,
            alignment=Alignment.TopLeft,
        )

        x_current += self._question_explanation_element.width
        self.draw_vertical_separator(dwg, x_current, y, height_container, self._color)
        self.draw_element(
            dwg=dwg,
            element=self._priority_details_element,
            x_container=x_current,
            y_container=y,
            width_container=self._priority_details_element.width,
            height_container=height_container,
            alignment=Alignment.TopLeft,
        )

        x_current += self._priority_details_element.width
        self.draw_vertical_separator(dwg, x_current, y, height_container, self._color)
        self.draw_element(
            dwg=dwg,
            element=self._organisation_details_element,
            x_container=x_current,
            y_container=y,
            width_container=self._organisation_details_element.width,
            height_container=height_container,
            alignment=Alignment.TopLeft,
        )

        x_current += self._organisation_details_element.width
        self.draw_vertical_separator(dwg, x_current, y, height_container, self._color)
        self.draw_element(
            dwg=dwg,
            element=self._related_element,
            x_container=x_current,
            y_container=y,
            width_container=self._related_element.width,
            height_container=height_container,
            alignment=Alignment.TopLeft,
        )

    def draw_last_lines(self, dwg: Drawing, x: float, y: float):
        dwg.add(
            wrapped_text(
                dwg,
                self._last_line_keywords,
                insert=(
                    x + self.layout_configuration.small_margin,
                    y + self.layout_configuration.small_margin,
                ),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                text_anchor="left",
                dominant_baseline="text-before-edge",
            )
        )
