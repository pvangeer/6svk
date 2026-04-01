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

from pydantic import model_validator, PrivateAttr
from svgwrite import Drawing

from svk.data import ResearchQuestion
from svk.visualization.helpers._wrappedtext import wrapped_text, wrapped_lines
from svk.visualization.helpers._greyfraction import color_toward_grey
from svk.visualization.elements._visual_elements_container import VisualElementsContainer, Alignment
from svk.visualization.elements._question_details import IdElement, PriorityIconElement
from svk.visualization.elements._wrapped_text_element import WrappedTextElement
from svk.visualization.helpers._measuretext import measure_text


class QuestionSummaryElement(VisualElementsContainer):
    """
    Represents a question element (as part of  a group, column and the overview page)
    """

    research_question: ResearchQuestion
    """The research question"""
    page_number: int

    _height: float = PrivateAttr()
    _width: float = PrivateAttr()

    _id_element: IdElement = PrivateAttr()
    _priority_icon_element: PriorityIconElement = PrivateAttr()
    _question_element: WrappedTextElement = PrivateAttr()

    _lines: list[str] = []

    @model_validator(mode="after")
    def validate(self):
        self._id_element = IdElement(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            id=self.research_question.id,
            translator=self.translator,
        )
        self._priority_icon_element = PriorityIconElement(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            priority=self.research_question.priority,
            translator=self.translator,
        )
        self._question_element = WrappedTextElement(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            max_width=self.layout_configuration.summary_question_lines_width,
            text=self.research_question.question,
        )
        self._width = self._id_element.width + self._priority_icon_element.width + self._question_element.width
        self._height = max([self._id_element.height, self._priority_icon_element.height, self._question_element.height])

        return self

    @property
    def height(self) -> float:
        return self._height

    @property
    def width(self) -> float:
        return self._width

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

        x_current = x
        self.draw_element(
            dwg=dwg,
            element=self._priority_icon_element,
            x_container=x_current,
            y_container=y,
            width_container=self._priority_icon_element.width,
            height_container=self.height,
            alignment=Alignment.MiddleCenter,
        )

        x_current += self._priority_icon_element.width
        self.draw_vertical_separator(dwg, x_current, y, self.height, self._color)

        self.draw_element(
            dwg=dwg,
            element=self._id_element,
            x_container=x_current,
            y_container=y,
            width_container=self._id_element.width,
            height_container=self.height,
            alignment=Alignment.MiddleCenter,
        )

        x_current += self._id_element.width
        # TODO: Move this to the id element? Both registering a link as well as a target?
        text_w, _ = measure_text(text=self.research_question.id, font_size=self.layout_configuration.font_size)
        x_id_middle = x_current - self._id_element.width / 2.0
        self.links_register.register_link(
            link_target=self.research_question.id,
            page_number=self.page_number,
            x=x_id_middle - text_w / 2.0,
            y=y + self.height / 2.0 - self.layout_configuration.font_size / 2,
            width=text_w,
            height=self.layout_configuration.font_size,
        )

        self.draw_vertical_separator(dwg, x_current, y, self.height, self._color)

        self.draw_element(
            dwg=dwg,
            element=self._question_element,
            x_container=x_current,
            y_container=y,
            width_container=self._id_element.width,
            height_container=self.height,
            alignment=Alignment.TopLeft,
        )
