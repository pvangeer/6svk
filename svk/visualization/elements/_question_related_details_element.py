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
from svk.visualization.elements._visual_elements_container import VisualElementsContainer
from svk.visualization.helpers._draw_scaled_icon import draw_scaled_icon


class QuestionRelatedDetailsElement(VisualElementsContainer):
    research_question: ResearchQuestion
    """The research question"""
    color: str
    page_number: int
    related_title: Label = Label.QD_Related

    _height: float = PrivateAttr()
    _width: float = PrivateAttr()

    @model_validator(mode="after")
    def validate(self) -> QuestionRelatedDetailsElement:
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
