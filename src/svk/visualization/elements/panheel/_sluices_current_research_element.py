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
from svk.data import SluicesResearchQuestion, Label, Color
from svk.visualization.elements._title_element import TitleElement
from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.elements._visual_elements_container import VisualElementsContainer, Alignment
from svk.visualization.elements._wrapped_text_element import WrappedTextElement


class CurrentResearchDetailsElement(VisualElementsContainer):
    research_question: SluicesResearchQuestion
    """The research question"""
    color: Color

    _title_element: TitleElement = PrivateAttr()

    def measure(self) -> None:
        self._title_element = self.create(
            TitleElement,
            title=Label.QD_CurrentResearch,
        )

        self._related_research_element = self.create(
            WrappedTextElement,
            text=self.research_question.related_research if self.research_question.related_research is not None else "-",
            has_margins=False,
            max_width=self.layout_configuration.current_research_details_width - self.layout_configuration.small_margin * 5,
        )

        self._research_program_element = self.create(
            WrappedTextElement,
            text=self.research_question.research_program if self.research_question.research_program is not None else "-",
            has_margins=False,
            max_width=self.layout_configuration.current_research_details_width - self.layout_configuration.small_margin * 5,
        )

        self._width = max(
            [
                self._title_element.width,
                self.layout_configuration.current_research_details_width,
                (
                    self.layout_configuration.small_margin
                    + max(
                        [
                            measure_text(
                                (self.translator.get_label(Label.QD_RelatedResearch) + ": "),
                                self.layout_configuration.font_size,
                            )[0],
                            measure_text(
                                (self.translator.get_label(Label.QD_AdressedInResearchProject) + ": "),
                                self.layout_configuration.font_size,
                            )[0],
                        ]
                    )
                    + self.layout_configuration.small_margin
                ),
            ]
        )
        self._height = (
            self._title_element.height
            + self.layout_configuration.small_margin
            + self.layout_configuration.font_size * 1.2
            + self._research_program_element.height
            + self.layout_configuration.font_size * 1.2
            + self._related_research_element.height
            + self.layout_configuration.small_margin
        )

    def _draw(self, x: float, y: float):
        self._title_element.draw(self._dwg, x, y)

        y += self._title_element.height
        self.draw_horizontal_separator(x, y, self.width, self.color)

        y_current = y + self.layout_configuration.small_margin
        self._dwg.add(
            self._dwg.text(
                self.translator.get_label(Label.QD_AdressedInResearchProject) + ":",
                insert=(
                    x + self.layout_configuration.small_margin,
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
        self.draw_element(
            element=self._research_program_element,
            x_container=x + self.layout_configuration.small_margin * 4,
            y_container=y_current,
            width_container=self._research_program_element.width,
            height_container=self._research_program_element.height,
            alignment=Alignment.TopLeft,
        )
        y_current += self._research_program_element.height

        self._dwg.add(
            self._dwg.text(
                self.translator.get_label(Label.QD_RelatedResearch) + ":",
                insert=(
                    x + self.layout_configuration.small_margin,
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
        self.draw_element(
            element=self._related_research_element,
            x_container=x + self.layout_configuration.small_margin * 4,
            y_container=y_current,
            width_container=self._research_program_element.width,
            height_container=self._research_program_element.height,
            alignment=Alignment.TopLeft,
        )
