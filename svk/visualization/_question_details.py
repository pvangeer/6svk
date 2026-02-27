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

from pydantic import Field, model_validator
from svk.data import ResearchQuestion, Priority, Label
from svgwrite import Drawing
from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.helpers._wrappedtext import wrapped_text, wrapped_lines
from svk.visualization.helpers._greyfraction import color_toward_grey
from svk.visualization._visual_element import VisualElement
from svk.visualization.helpers._draw_priority_arrow import draw_priority_arrow


class QuestionDetails(VisualElement):
    research_question: ResearchQuestion
    """The research question"""

    height: float = Field(default_factory=int)
    w_code_field: float = Field(default_factory=float)
    w_relation_field: float = Field(default_factory=float)
    w_priority_field_fixed: float = Field(default_factory=float)
    w_priority_field: float = Field(default_factory=float)
    h_first_line: float = Field(default_factory=float)
    priority_explained_lines: list[str] = Field(default_factory=list[str])
    w_question_field: float = Field(default_factory=float)
    question_lines: list[str] = Field(default_factory=list[str])
    question_explained_lines: list[str] = Field(default_factory=list[str])

    related_title: Label = Label.QD_Related
    priority_title: Label = Label.QD_Priority

    def construct_lines(self):

        self._lines = wrapped_lines(
            self.research_question.question,
            max_width=self.layout_configuration.details_page_width
            - self.layout_configuration.paper_margin * 2
            - self.layout_configuration.question_id_box_width
            - 2 * self.layout_configuration.small_margin,
            font_size=self.layout_configuration.font_size,
        )

    @model_validator(mode="after")
    def compute_dimensions(self):
        self.w_code_field = max(
            self.layout_configuration.question_priority_box_width + self.layout_configuration.small_margin * 2,
            self.layout_configuration.question_id_box_width,
        )

        self.h_first_line = (
            self.layout_configuration.small_margin + self.layout_configuration.font_size + self.layout_configuration.small_margin
        )
        h_code_field = (
            self.h_first_line + self.layout_configuration.question_priority_box_width + self.layout_configuration.intermediate_margin
        )
        self.w_relation_field = max(
            measure_text(self.translator.get_label(self.related_title), self.layout_configuration.font_size)[0]
            + 2 * self.layout_configuration.small_margin,
            self.layout_configuration.question_id_box_width + 2 * self.layout_configuration.small_margin,
        )
        h_relation_field = (
            self.h_first_line
            + len(self.research_question.reference_ids) * self.layout_configuration.font_size * 1.2
            + self.layout_configuration.small_margin
        )
        self.w_priority_field_fixed = 50
        h_priority_fixed_field = self.h_first_line + 4 * self.layout_configuration.font_size * 1.2 + self.layout_configuration.small_margin
        w_remaining = (
            self.layout_configuration.details_page_width
            - self.layout_configuration.paper_margin * 2.0
            - self.w_code_field
            - self.w_priority_field_fixed
            - self.w_relation_field
        )
        self.w_priority_field = w_remaining * 0.4
        self.priority_explained_lines = []
        h_priority_field = (
            self.h_first_line
            + len(self.priority_explained_lines) * self.layout_configuration.font_size * 1.2
            + self.layout_configuration.small_margin
        )

        self.w_question_field = w_remaining * 0.6
        self.question_lines = wrapped_lines(
            self.research_question.question,
            self.w_question_field - 2 * self.layout_configuration.small_margin,
            self.layout_configuration.font_size,
        )
        self.question_explained_lines = wrapped_lines(
            "-" if self.research_question.explanation is None else str(self.research_question.explanation),
            self.w_question_field - 2 * self.layout_configuration.small_margin,
            self.layout_configuration.font_size,
        )
        h_question_field = (
            self.layout_configuration.small_margin
            + len(self.question_lines) * self.layout_configuration.font_size * 1.2
            + self.layout_configuration.small_margin
            + len(self.question_explained_lines) * self.layout_configuration.font_size * 1.2
            + self.layout_configuration.small_margin
        )

        self.height = max(h_code_field, h_priority_field, h_priority_fixed_field, h_question_field, h_relation_field)

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

    def draw(self, dwg: Drawing, x: float, y: float, width: float, page_number: int):
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

        dwg.add(
            dwg.text(
                self.research_question.id,
                insert=(x + self.w_code_field / 2.0, y + self.layout_configuration.small_margin),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                text_anchor="middle",
                dominant_baseline="text-before-edge",
            )
        )

        prio_symbol_height = self.height - self.h_first_line

        dwg.add(
            dwg.line(
                start=(x + self.layout_configuration.small_margin, y + self.h_first_line),
                end=(x + self.w_code_field - self.layout_configuration.small_margin, y + self.h_first_line),
                stroke_width=0.5,
                stroke=self._color,
            )
        )

        y_middle = (
            y
            + self.layout_configuration.small_margin
            + self.layout_configuration.small_margin
            + self.layout_configuration.font_size * 1.2
            + prio_symbol_height / 2.0
        )
        x_id_left = x + self.w_code_field / 2 - self.layout_configuration.question_priority_box_width / 2
        if not self.research_question.has_priority:
            draw_priority_arrow(dwg, x=x_id_left, y=y_middle, width=self.layout_configuration.question_priority_box_width)
        else:
            draw_priority_arrow(
                dwg,
                x=x_id_left,
                y=y_middle - 2.5,
                width=self.layout_configuration.question_priority_box_width,
            )
            draw_priority_arrow(
                dwg,
                x=x_id_left,
                y=y_middle + 2.5,
                width=self.layout_configuration.question_priority_box_width,
            )

        self.draw_vertical_separator(dwg, x + self.w_code_field, y, self.height, self._color)

        dwg.add(
            wrapped_text(
                dwg,
                self.question_lines,
                insert=(x + self.w_code_field + self.layout_configuration.small_margin, y + self.layout_configuration.small_margin),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_style="italic",
                font_weight="normal",
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )

        dwg.add(
            wrapped_text(
                dwg,
                self.question_explained_lines,
                insert=(
                    x + self.w_code_field + self.layout_configuration.small_margin,
                    y
                    + self.layout_configuration.small_margin
                    + len(self.question_lines) * self.layout_configuration.font_size * 1.2
                    + self.layout_configuration.small_margin,
                ),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )

        self.draw_vertical_separator(dwg, x + self.w_code_field + self.w_question_field, y, self.height, self._color)

        x_priority = x + self.w_code_field + self.w_question_field
        dwg.add(
            dwg.text(
                self.translator.get_label(self.priority_title),
                insert=(
                    x_priority + self.layout_configuration.small_margin,
                    y + self.layout_configuration.small_margin,
                ),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )

        dwg.add(
            dwg.line(
                start=(x_priority + self.layout_configuration.small_margin, y + self.h_first_line),
                end=(
                    x_priority + self.w_priority_field + self.w_priority_field_fixed - self.layout_configuration.small_margin,
                    y + self.h_first_line,
                ),
                stroke_width=0.5,
                stroke=self._color,
            )
        )

        prios = [
            (Label.QD_WaterSafety, self.research_question.prio_water_safety),
            (Label.QD_OtherFunctions, self.research_question.prio_other_functions),
            (Label.QD_Operation, self.research_question.prio_operation),
            (Label.QD_Maitenance, self.research_question.prio_management_maintenance),
        ]
        prios_translated = [(self.translator.get_label(p[0]) + ":", p[1]) for p in prios]
        max_label_width = max([measure_text(p[0], self.layout_configuration.font_size)[0] for p in prios_translated])
        y_prio_current = y + self.h_first_line + self.layout_configuration.small_margin
        x_prio_label = x_priority + self.layout_configuration.small_margin
        x_prio_first = x_prio_label + max_label_width + self.layout_configuration.small_margin
        for prio in prios_translated:
            dwg.add(
                dwg.text(
                    prio[0],
                    insert=(
                        x_prio_label,
                        y_prio_current,
                    ),
                    font_size=self.layout_configuration.font_size,
                    font_family="Arial",
                    font_weight="normal",
                    text_anchor="start",
                    dominant_baseline="text-before-edge",
                )
            )
            self.draw_priority_dots(dwg, x_prio_first, y_prio_current, prio[1])
            y_prio_current += self.layout_configuration.font_size * 1.2

        x_related_start = x + self.w_code_field + self.w_question_field + self.w_priority_field_fixed + self.w_priority_field
        self.draw_vertical_separator(
            dwg,
            x_related_start,
            y,
            self.height,
            self._color,
        )

        dwg.add(
            dwg.text(
                self.translator.get_label(self.related_title),
                insert=(
                    x_related_start + self.layout_configuration.small_margin,
                    y + self.layout_configuration.small_margin,
                ),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )

        dwg.add(
            dwg.line(
                start=(x_related_start + self.layout_configuration.small_margin, y + self.h_first_line),
                end=(
                    x_related_start + self.w_relation_field - self.layout_configuration.small_margin,
                    y + self.h_first_line,
                ),
                stroke_width=0.5,
                stroke=self._color,
            )
        )

        x_related = x_related_start + self.layout_configuration.small_margin
        y_related_current = y + self.h_first_line + self.layout_configuration.small_margin
        for related in self.research_question.reference_ids:
            dwg.add(
                dwg.text(
                    related,
                    insert=(
                        x_related,
                        y_related_current,
                    ),
                    font_size=self.layout_configuration.font_size,
                    font_family="Arial",
                    font_weight="normal",
                    text_anchor="start",
                    dominant_baseline="text-before-edge",
                )
            )
            self.links_register.register_link(
                link_target=related,
                page_number=page_number,
                x=x_related,
                y=y_related_current,
                width=measure_text(related, self.layout_configuration.font_size)[0],
                height=self.layout_configuration.font_size,
            )
            y_related_current += self.layout_configuration.font_size * 1.2

    def draw_priority_dots(self, dwg: Drawing, x: float, y_current: float, prio: Priority):
        dotradius = 5
        y_center = y_current + self.layout_configuration.font_size - dotradius
        x_prio_first = x + dotradius
        x_prio_second = x_prio_first + dotradius * 2.5
        x_prio_third = x_prio_second + dotradius * 2.5

        match prio:
            case Priority.High:
                dwg.add(dwg.circle(center=(x_prio_first, y_center), r=dotradius, fill="black"))
                dwg.add(dwg.circle(center=(x_prio_second, y_center), r=dotradius, fill="black"))
                dwg.add(dwg.circle(center=(x_prio_third, y_center), r=dotradius, fill="black"))
            case Priority.Medium:
                dwg.add(dwg.circle(center=(x_prio_first, y_center), r=dotradius, fill="black"))
                dwg.add(dwg.circle(center=(x_prio_second, y_center), r=dotradius, fill="black"))
            case Priority.Low:
                dwg.add(dwg.circle(center=(x_prio_first, y_center), r=dotradius, fill="black"))
            case Priority.Unknown:
                dwg.add(
                    dwg.text(
                        "?",
                        insert=(x, y_current),
                        font_size=self.layout_configuration.font_size,
                        font_family="Arial",
                        font_weight="normal",
                        text_anchor="start",
                        dominant_baseline="text-before-edge",
                    )
                )
