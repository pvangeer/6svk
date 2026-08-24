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
from svk.data import SluicesResearchQuestion, Label
from svk.visualization.elements._title_element import TitleElement
from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.elements._visual_elements_container import VisualElementsContainer, Alignment
from svk.visualization.elements._wrapped_text_element import WrappedTextElement


class CurrentResearchDetailsElement(VisualElementsContainer):
    research_question: SluicesResearchQuestion
    """The research question"""
    color: str

    _width: float = PrivateAttr()
    _height: float = PrivateAttr()
    _title_element: TitleElement = PrivateAttr()

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    @model_validator(mode="after")
    def validate(self) -> CurrentResearchDetailsElement:
        self._title_element = TitleElement(
            title=Label.QD_CurrentResearch,
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
        )

        self._related_research_element = WrappedTextElement(
            text=self.research_question.related_research if self.research_question.related_research is not None else "-",
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            has_margins=False,
            max_width=self.layout_configuration.current_research_details_width - self.layout_configuration.small_margin * 5,
        )

        self._research_program_element = WrappedTextElement(
            text=self.research_question.research_program if self.research_question.research_program is not None else "-",
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
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
        return self

    def draw(self, dwg: Drawing, x: float, y: float):
        self._title_element.draw(dwg, x, y)

        y += self._title_element.height
        self.draw_horizontal_separator(dwg, x, y, self.width, self.color)

        y_current = y + self.layout_configuration.small_margin
        dwg.add(
            dwg.text(
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
            dwg=dwg,
            element=self._research_program_element,
            x_container=x + self.layout_configuration.small_margin * 4,
            y_container=y_current,
            width_container=self._research_program_element.width,
            height_container=self._research_program_element.height,
            alignment=Alignment.TopLeft,
        )
        y_current += self._research_program_element.height

        dwg.add(
            dwg.text(
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
            dwg=dwg,
            element=self._related_research_element,
            x_container=x + self.layout_configuration.small_margin * 4,
            y_container=y_current,
            width_container=self._research_program_element.width,
            height_container=self._research_program_element.height,
            alignment=Alignment.TopLeft,
        )
