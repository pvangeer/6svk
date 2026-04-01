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
from svk.data import ResearchQuestion, Priority, Label
from svgwrite import Drawing
from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.helpers._wrappedtext import wrapped_text, wrapped_lines
from svk.visualization.elements._visual_elements_container import VisualElementsContainer


class QuestionPriorityDetailsElement(VisualElementsContainer):
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
    def validate(self) -> QuestionPriorityDetailsElement:
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
