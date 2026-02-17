"""
Copyright (C) Stichting Deltares 2026. All rights reserved.

This file is part of the dikernel-python toolbox.

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

from pydantic import model_validator, Field
from svgwrite import Drawing

from svk.data import ResearchQuestion
from svk.visualization.helpers._drawwrappedtext import wrapped_text, wrapped_lines
from svk.visualization.helpers._greyfraction import color_toward_grey
from svk.visualization.helpers._draw_priority_arrow import draw_priority_arrow
from svk.visualization._visual_element import VisualElement
from svk.visualization.helpers._measuretext import measure_text


class Question(VisualElement):
    """
    Represents a question element (as part of  a group, column and the figure)
    """

    research_question: ResearchQuestion
    """The research question"""
    height: float = Field(default_factory=int)

    _lines: list[str] = []

    def construct_lines(self):
        self._lines = wrapped_lines(
            self.research_question.question,
            max_width=self.layout_configuration.column_width
            - self.layout_configuration.arrow_depth
            - 2 * self.layout_configuration.element_margin
            - 2 * self.layout_configuration.line_margin
            - self._id_box_width
            - self._priority_box_width,
            font_size=self.layout_configuration.font_size,
        )

    @model_validator(mode="after")
    def compute_height(self):
        self.construct_lines()
        self.height = self.layout_configuration.font_size * len(self._lines) * 1.2 + self.layout_configuration.line_margin * 2.0

        return self

    @property
    def high_priority(self) -> bool:
        return (
            self.research_question.prio_management_maintenance.id == 3
            or self.research_question.prio_water_safety.id == 3
            or self.research_question.prio_operation.id == 3
            or (
                self.research_question.prio_management_maintenance.id
                + self.research_question.prio_operation.id
                + self.research_question.prio_water_safety.id
                + self.research_question.prio_other_functions.id
            )
            > 8
        )

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

    @property
    def _id_box_width(self) -> float:
        return (
            self.layout_configuration.question_id_box_width + self.layout_configuration.line_margin + self.layout_configuration.line_margin
        )

    @property
    def _priority_box_width(self) -> float:
        return (
            self.layout_configuration.question_priority_box_width
            + self.layout_configuration.line_margin
            + self.layout_configuration.line_margin
        )

    def draw(self, dwg: Drawing, x: float, y: float, width: float):
        dwg.add(
            dwg.rect(
                insert=(x, y),
                size=(width, self.height),
                stroke_width=0.5,
                fill=self._color,
                fill_opacity=0.3,
                stroke=self._color,
            )
        )

        y_middle = y + self.height / 2
        if not self.high_priority:
            draw_priority_arrow(
                dwg, x=x + self.layout_configuration.line_margin, y=y_middle, width=self.layout_configuration.question_priority_box_width
            )
        else:
            draw_priority_arrow(
                dwg,
                x=x + self.layout_configuration.line_margin,
                y=y_middle - 2.5,
                width=self.layout_configuration.question_priority_box_width,
            )
            draw_priority_arrow(
                dwg,
                x=x + self.layout_configuration.line_margin,
                y=y_middle + 2.5,
                width=self.layout_configuration.question_priority_box_width,
            )

        if len(self._lines) < 1:
            self.construct_lines()

        text_w, _ = measure_text(text=self.research_question.id, font_size=10)
        self.links_manager.register_link(
            link_target=self.research_question.id,
            page_number=0,
            x=x + self._priority_box_width,
            y=y + self.height / 2 - 6.0,
            width=text_w,
            height=12.0,
        )

        dwg.add(
            dwg.text(
                self.research_question.id,
                insert=(
                    x + self._priority_box_width,
                    y + self.height / 2,
                ),
                text_anchor="start",
                font_family="Arial",
                dominant_baseline="middle",
                font_size=10,
            )
        )

        dwg.add(
            wrapped_text(
                dwg,
                lines=self._lines,
                insert=(x + self._priority_box_width + self._id_box_width, y + self.layout_configuration.line_margin),
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )

        pass
