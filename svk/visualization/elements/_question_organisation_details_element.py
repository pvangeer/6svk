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
from svk.data import ResearchQuestion, Label, ResearchLine
from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.elements._visual_elements_container import VisualElementsContainer


class QuestionOrganisationDetailsElement(VisualElementsContainer):
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
    def validate(self) -> QuestionOrganisationDetailsElement:
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
