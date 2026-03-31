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
from svk.data import ResearchQuestion, Priority, Label, ResearchLine
from svgwrite import Drawing
from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.helpers._wrappedtext import wrapped_text, wrapped_lines
from svk.visualization.helpers._greyfraction import color_toward_grey
from svk.visualization.elements._visual_element import VisualElement
from svk.visualization.elements._elements_container import VisualElementsContainer, Alignment
from svk.visualization.helpers._draw_priority_arrow import draw_priority_arrow
from svk.visualization.helpers._draw_scaled_icon import draw_scaled_icon


class QuestionDetailsPriorityElement(VisualElementsContainer):
    research_question: ResearchQuestion
    """The research question"""
    color: str
    dotradius: float = 5
    priority_title: Label = Label.QD_Priority

    _width: float = PrivateAttr()
    _height: float = PrivateAttr()
    _lines: list[str] = PrivateAttr()
    _w_priority_metrices_column: float = PrivateAttr()

    @property
    def height(self) -> float:
        return self._height

    @property
    def width(self) -> float:
        return self._width

    @model_validator(mode="after")
    def validate(self) -> QuestionDetailsPriorityElement:
        prio_labels = [Label.QD_WaterSafety, Label.QD_OtherFunctions, Label.QD_Operation, Label.QD_Maitenance]
        self._w_priority_metrices_column = (
            self.layout_configuration.small_margin
            + max([measure_text(self.translator.get_label(l) + ":", self.layout_configuration.font_size)[0] for l in prio_labels])
            + self.layout_configuration.small_margin
            + self.dotradius * 7
            + self.layout_configuration.small_margin
        )
        self._width = self.layout_configuration.details_priority_explanation_width + self._w_priority_metrices_column

        h_priority_column_fixed_items = (
            self.layout_configuration.small_margin
            + self.layout_configuration.font_size * 1.2
            + 2 * self.layout_configuration.small_margin
            + len(prio_labels) * self.layout_configuration.font_size * 1.2
            + self.layout_configuration.small_margin
        )

        self._lines = (
            wrapped_lines(
                self.research_question.prio_explanation,
                self.layout_configuration.details_priority_explanation_width - self.layout_configuration.small_margin * 2,
            )
            if self.research_question.prio_explanation is not None
            else []
        )

        h_priority_column_explained_lines = (
            self.layout_configuration.small_margin
            + self.layout_configuration.font_size * 1.2
            + 2 * self.layout_configuration.small_margin
            + len(self._lines) * self.layout_configuration.font_size * 1.2
            + self.layout_configuration.small_margin
        )

        self._height = max([h_priority_column_fixed_items, h_priority_column_explained_lines])
        return self

    def draw(self, dwg: Drawing, x: float, y: float):
        dwg.add(
            dwg.text(
                self.translator.get_label(self.priority_title),
                insert=(
                    x + self.layout_configuration.small_margin,
                    y + self.layout_configuration.small_margin,
                ),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )

        y_prios_start = y + self.layout_configuration.font_size * 1.2 + 2 * self.layout_configuration.small_margin
        self.draw_horizontal_separator(
            dwg,
            x,
            y_prios_start,
            self.width,
            self.color,
        )

        prios = [
            (Label.QD_WaterSafety, self.research_question.prio_water_safety),
            (Label.QD_OtherFunctions, self.research_question.prio_other_functions),
            (Label.QD_Operation, self.research_question.prio_operation),
            (Label.QD_Maitenance, self.research_question.prio_management_maintenance),
        ]
        prios_translated = [(self.translator.get_label(p[0]) + ":", p[1]) for p in prios]
        max_label_width = max([measure_text(p[0], self.layout_configuration.font_size)[0] for p in prios_translated])
        y_prio_current = y_prios_start + self.layout_configuration.small_margin
        x_prio_label = x + self.layout_configuration.small_margin
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

        self.draw_vertical_separator(
            dwg,
            x + self._w_priority_metrices_column,
            y_prios_start,
            self.height - self.layout_configuration.small_margin * 2 - self.layout_configuration.font_size * 1.2,
            self.color,
        )

        if self._lines:
            dwg.add(
                wrapped_text(
                    dwg=dwg,
                    lines=self._lines,
                    insert=(
                        x + self._w_priority_metrices_column + self.layout_configuration.small_margin,
                        y_prios_start + self.layout_configuration.small_margin,
                    ),
                    font_size=self.layout_configuration.font_size,
                    dominant_baseline="text-before-edge",
                )
            )

    def draw_priority_dots(self, dwg: Drawing, x: float, y_current: float, prio: Priority):
        y_center = y_current + self.layout_configuration.font_size - self.dotradius
        x_prio_first = x + self.dotradius
        x_prio_second = x_prio_first + self.dotradius * 2.5
        x_prio_third = x_prio_second + self.dotradius * 2.5

        match prio:
            case Priority.High:
                dwg.add(dwg.circle(center=(x_prio_first, y_center), r=self.dotradius, fill="black"))
                dwg.add(dwg.circle(center=(x_prio_second, y_center), r=self.dotradius, fill="black"))
                dwg.add(dwg.circle(center=(x_prio_third, y_center), r=self.dotradius, fill="black"))
            case Priority.Medium:
                dwg.add(dwg.circle(center=(x_prio_first, y_center), r=self.dotradius, fill="black"))
                dwg.add(dwg.circle(center=(x_prio_second, y_center), r=self.dotradius, fill="black"))
            case Priority.Low:
                dwg.add(dwg.circle(center=(x_prio_first, y_center), r=self.dotradius, fill="black"))
            case Priority.No:
                dwg.add(
                    dwg.text(
                        "-",
                        insert=(x, y_current),
                        font_size=self.layout_configuration.font_size,
                        font_family="Arial",
                        font_weight="normal",
                        text_anchor="start",
                        dominant_baseline="text-before-edge",
                    )
                )
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


class QuestionDetailsRelatedElement(VisualElementsContainer):
    research_question: ResearchQuestion
    """The research question"""
    color: str
    page_number: int
    related_title: Label = Label.QD_Related

    _height: float = PrivateAttr()
    _width: float = PrivateAttr()

    @model_validator(mode="after")
    def validate(self) -> QuestionDetailsRelatedElement:
        w_related_title = (
            self.layout_configuration.small_margin
            + measure_text(self.translator.get_label(self.related_title), self.layout_configuration.font_size)[0]
            + self.layout_configuration.small_margin
        )
        # TODO: Move this to another part of the details?
        w_related_barrier_icons: float = 2 * self.layout_configuration.small_margin + self.layout_configuration.icon_width_small
        w_related_questions: float = self.layout_configuration.question_id_box_width

        self._width = max(
            w_related_title,
            w_related_questions + w_related_barrier_icons,
        )

        self._height = (
            self.layout_configuration.small_margin
            + self.layout_configuration.font_size * 1.2
            + 2 * self.layout_configuration.small_margin
            + max(
                len(self.research_question.reference_ids) * self.layout_configuration.font_size * 1.2
                + self.layout_configuration.small_margin,
                len(self.research_question.storm_surge_barriers)
                * (self.layout_configuration.icon_width_small + self.layout_configuration.small_margin),
            )
        )
        return self

    @property
    def height(self) -> float:
        return self._height

    @property
    def width(self) -> float:
        return self._width

    def draw(self, dwg: Drawing, x: float, y: float):
        x_related_start = x

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

        y_hline = y + self.layout_configuration.font_size * 1.2 + 2 * self.layout_configuration.small_margin
        self.draw_horizontal_separator(dwg=dwg, x=x_related_start, y=y_hline, element_width=self.width, color=self.color)

        x_icons = x_related_start + self.layout_configuration.small_margin
        y_icon_current = y_hline + self.layout_configuration.small_margin
        for barrier in self.research_question.storm_surge_barriers:
            draw_scaled_icon(
                dwg=dwg,
                storm_surge_barrier=barrier,
                insert=(
                    x_icons,
                    y_icon_current,
                ),
                size=(self.layout_configuration.icon_width_small, self.layout_configuration.icon_width_small),
            )
            y_icon_current += self.layout_configuration.icon_width_small + self.layout_configuration.small_margin

        x_related = x_related_start + 2 * self.layout_configuration.small_margin + self.layout_configuration.icon_width_small
        self.draw_vertical_separator(
            dwg=dwg,
            x=x_related,
            y=y_hline,
            element_height=self.height - (self.layout_configuration.font_size * 1.2 + 2 * self.layout_configuration.small_margin),
            color=self.color,
        )

        x_related += self.layout_configuration.small_margin
        y_related_current = y_hline + self.layout_configuration.small_margin
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
                page_number=self.page_number,
                x=x_related,
                y=y_related_current,
                width=measure_text(related, self.layout_configuration.font_size)[0],
                height=self.layout_configuration.font_size,
            )
            y_related_current += self.layout_configuration.font_size * 1.2


class QuestionDetailsOrganisationElement(VisualElementsContainer):
    research_question: ResearchQuestion
    """The research question"""
    color: str
    page_number: int
    organizational_title: Label = Label.QD_Organizational

    _width: float = PrivateAttr()
    _height: float = PrivateAttr()

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    @model_validator(mode="after")
    def validate(self) -> QuestionDetailsOrganisationElement:
        fixed_fields: list[tuple[Label, float]] = [
            (Label.QD_ResearchLineOne, self._get_max_research_line_title_length()),
            (Label.QD_ResearchLineTwo, self._get_max_research_line_title_length()),
            (Label.QD_Status, 0),  # TODO: Read status from database
            (
                (
                    Label.QD_ActionHolder,
                    (
                        measure_text(self.research_question.action_holder, self.layout_configuration.font_size)[0]
                        if self.research_question.action_holder is not None
                        else 0.0
                    ),
                )
            ),
        ]
        self._width = (
            self.layout_configuration.small_margin
            + max(
                [
                    measure_text(
                        (self.translator.get_label(l[0]) + ": "),
                        self.layout_configuration.font_size,
                    )[0]
                    + l[1]
                    for l in fixed_fields
                ]
            )
            + self.layout_configuration.small_margin
        )
        self._height = (
            self.layout_configuration.small_margin
            + self.layout_configuration.font_size * 1.2
            + self.layout_configuration.small_margin * 2
            + self.layout_configuration.font_size * 1.2 * 4
            + self.layout_configuration.small_margin
        )
        return self

    def draw(self, dwg: Drawing, x: float, y: float):
        x_organisational = x
        dwg.add(
            dwg.text(
                self.translator.get_label(self.organizational_title),
                insert=(
                    x_organisational + self.layout_configuration.small_margin,
                    y + self.layout_configuration.small_margin,
                ),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )

        y_org_start = y + self.layout_configuration.font_size * 1.2 + 3 * self.layout_configuration.small_margin

        self.draw_horizontal_separator(dwg, x_organisational, y_org_start - self.layout_configuration.small_margin, self.width, self.color)

        y_current = y_org_start
        # status = self.research_question.status if self.research_question.status is not None else ""
        # TODO: Read status from database
        status = ""
        dwg.add(
            dwg.text(
                self.translator.get_label(Label.QD_Status) + ": " + status,
                insert=(
                    x_organisational + self.layout_configuration.small_margin,
                    y_current,
                ),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )

        y_current += self.layout_configuration.font_size * 1.2
        action_holder = self.research_question.action_holder if self.research_question.action_holder is not None else ""
        dwg.add(
            dwg.text(
                self.translator.get_label(Label.QD_ActionHolder) + ": " + action_holder,
                insert=(
                    x_organisational + self.layout_configuration.small_margin,
                    y_current,
                ),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )

        y_current += self.layout_configuration.font_size * 1.2
        self._draw_research_line_link(
            dwg=dwg,
            page_number=self.page_number,
            x_start=x_organisational + self.layout_configuration.small_margin,
            y_start=y_current,
            research_line=self.research_question.research_line_primary,
            label=Label.QD_ResearchLineOne,
        )

        y_current += self.layout_configuration.font_size * 1.2
        self._draw_research_line_link(
            dwg=dwg,
            page_number=self.page_number,
            x_start=x_organisational + self.layout_configuration.small_margin,
            y_start=y_current,
            research_line=self.research_question.research_line_secondary,
            label=Label.QD_ResearchLineTwo,
        )

    def _get_max_research_line_title_length(self) -> float:
        return max(
            [measure_text(self.translator.get_label(line.title), self.layout_configuration.font_size)[0] for line in list(ResearchLine)]
        )

    def _draw_research_line_link(
        self, dwg: Drawing, page_number: int, x_start: float, y_start: float, research_line: ResearchLine | None, label: Label
    ):
        link_text = self.translator.get_label(research_line.title) if research_line is not None else ""
        dwg.add(
            dwg.text(
                self.translator.get_label(label) + ": " + link_text,
                insert=(
                    x_start,
                    y_start,
                ),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )

        if research_line is not None:
            self.links_register.register_link(
                link_target=research_line.id,
                page_number=page_number,
                x=x_start + measure_text(self.translator.get_label(label) + ": ", self.layout_configuration.font_size)[0],
                y=y_start,
                width=measure_text(link_text, self.layout_configuration.font_size)[0],
                height=self.layout_configuration.font_size * 1.2,
            )


class QuestionDetailsExplanationElement(VisualElement):
    research_question: ResearchQuestion
    """The research question"""

    _height: float = PrivateAttr()

    @property
    def width(self) -> float:
        return self.layout_configuration.question_explanation_width

    @property
    def height(self) -> float:
        return 0.0

    @model_validator(mode="after")
    def validate(self) -> QuestionDetailsExplanationElement:
        self._lines = wrapped_lines(
            "-" if self.research_question.explanation is None else str(self.research_question.explanation),
            self.layout_configuration.question_explanation_width - 2 * self.layout_configuration.small_margin,
            self.layout_configuration.font_size,
        )

        self._height = (
            self.layout_configuration.small_margin
            + len(self._lines) * self.layout_configuration.font_size * 1.2
            + self.layout_configuration.small_margin
        )

        return self

    def draw(self, dwg: Drawing, x: float, y: float):
        dwg.add(
            wrapped_text(
                dwg,
                self._lines,
                insert=(
                    x + self.layout_configuration.small_margin,
                    y + self.layout_configuration.small_margin,
                ),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )


class QuestionDetailsPriorityIconElement(VisualElement):
    research_question: ResearchQuestion
    """The research question"""

    _height: float = PrivateAttr()
    _width: float = PrivateAttr()

    @property
    def height(self) -> float:
        return self._height

    @property
    def width(self) -> float:
        return self._width

    @model_validator(mode="after")
    def validate(self) -> QuestionDetailsPriorityIconElement:
        self._height = self.layout_configuration.question_priority_box_width + self.layout_configuration.intermediate_margin * 2
        self._width = self.layout_configuration.question_priority_box_width + self.layout_configuration.small_margin * 2
        return self

    def draw(self, dwg: Drawing, x: float, y: float):
        y_middle = y + self.height / 2.0
        x_arrows_left = x + self.layout_configuration.small_margin
        match self.research_question.priority:
            case 0:
                draw_priority_arrow(dwg, x=x_arrows_left, y=y_middle, width=self.layout_configuration.question_priority_box_width)
            case 1:
                draw_priority_arrow(
                    dwg,
                    x=x_arrows_left,
                    y=y_middle - 2.5,
                    width=self.layout_configuration.question_priority_box_width,
                )
                draw_priority_arrow(
                    dwg,
                    x=x_arrows_left,
                    y=y_middle + 2.5,
                    width=self.layout_configuration.question_priority_box_width,
                )
            case 2:
                draw_priority_arrow(
                    dwg,
                    x=x_arrows_left,
                    y=y_middle - 5,
                    width=self.layout_configuration.question_priority_box_width,
                )
                draw_priority_arrow(
                    dwg,
                    x=x_arrows_left,
                    y=y_middle,
                    width=self.layout_configuration.question_priority_box_width,
                )
                draw_priority_arrow(
                    dwg,
                    x=x_arrows_left,
                    y=y_middle + 5,
                    width=self.layout_configuration.question_priority_box_width,
                )
        pass


class QuestionDetailsIdElement(VisualElement):
    research_question: ResearchQuestion
    """The research question"""

    @property
    def width(self) -> float:
        return self.layout_configuration.question_id_box_width

    @property
    def height(self) -> float:
        return 2 * self.layout_configuration.small_margin + self.layout_configuration.font_size * 1.2

    def draw(self, dwg: Drawing, x: float, y: float):
        dwg.add(
            dwg.text(
                self.research_question.id,
                insert=(x + self.width / 2.0, y + self.layout_configuration.small_margin),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                text_anchor="middle",
                dominant_baseline="text-before-edge",
            )
        )
        pass


class QuestionDetailsElement(VisualElementsContainer):
    research_question: ResearchQuestion
    """The research question"""
    page_number: int

    _height: float = PrivateAttr()
    _width: float = PrivateAttr()

    _priority_icon_element: QuestionDetailsPriorityIconElement = PrivateAttr()
    _question_explanation_element: QuestionDetailsExplanationElement = PrivateAttr()
    _priority_element: QuestionDetailsPriorityElement = PrivateAttr()
    _organisation_element: QuestionDetailsOrganisationElement = PrivateAttr()
    _related_element: QuestionDetailsRelatedElement = PrivateAttr()
    _id_element: QuestionDetailsIdElement = PrivateAttr()

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
    def compute_dimensions(self):
        self._priority_icon_element = QuestionDetailsPriorityIconElement(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            research_question=self.research_question,
        )
        self._question_explanation_element = QuestionDetailsExplanationElement(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            research_question=self.research_question,
        )
        self._priority_element = QuestionDetailsPriorityElement(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            research_question=self.research_question,
            color=self._color,
        )
        self._organisation_element = QuestionDetailsOrganisationElement(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            research_question=self.research_question,
            color=self._color,
            page_number=self.page_number,
        )
        self._related_element = QuestionDetailsRelatedElement(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            research_question=self.research_question,
            color=self._color,
            page_number=self.page_number,
        )
        self._id_element = QuestionDetailsIdElement(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            research_question=self.research_question,
        )

        self._width = (
            max([self._priority_icon_element.width, self._id_element.width])
            + self._question_explanation_element.width
            + self._priority_element.width
            + self._organisation_element.width
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
                    self._priority_element.height,
                    self._organisation_element.height,
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
            element=self._priority_element,
            x_container=x_current,
            y_container=y,
            width_container=self._priority_element.width,
            height_container=height_container,
            alignment=Alignment.TopLeft,
        )

        x_current += self._priority_element.width
        self.draw_vertical_separator(dwg, x_current, y, height_container, self._color)
        self.draw_element(
            dwg=dwg,
            element=self._organisation_element,
            x_container=x_current,
            y_container=y,
            width_container=self._organisation_element.width,
            height_container=height_container,
            alignment=Alignment.TopLeft,
        )

        x_current += self._organisation_element.width
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
