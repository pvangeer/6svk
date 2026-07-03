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
from svk.visualization.helpers._wrappedtext import wrapped_lines, wrapped_text
from svk.visualization.elements._wrapped_bullet_list import WrappedBulletListElement
from svk.visualization.elements._visual_elements_container import VisualElementsContainer


class QuestionAnalysisDetailsElement(VisualElementsContainer):
    research_question: ResearchQuestion
    """The research question"""
    color: str
    page_number: int
    drivers_title: Label = Label.QD_Drivers
    functions_title: Label = Label.QD_Functions
    components_title: Label = Label.QD_Components
    
    # TODO: Implement
    _driver_lines: list[str] = PrivateAttr()
    _function_lines: list[str] = PrivateAttr()
    _component_lines: list[str] = PrivateAttr()
    _driver_element: WrappedBulletListElement = PrivateAttr()
    _function_element: WrappedBulletListElement = PrivateAttr()
    _component_element: WrappedBulletListElement = PrivateAttr()

    _height: float = PrivateAttr()
    _width: float = PrivateAttr()

    @model_validator(mode="after")
    def validate(self) -> QuestionAnalysisDetailsElement:
        self._driver_element = WrappedBulletListElement(
            max_width=self.layout_configuration.analysis_details_width,
            bullet_list=self.research_question.related_drivers.split(";") if self.research_question.related_drivers is not None else ["-"],
            layout_configuration=self.layout_configuration, 
            links_register=self.links_register, 
            translator=self.translator)
        self._function_element = WrappedBulletListElement(
            max_width=self.layout_configuration.analysis_details_width,
            bullet_list=self.research_question.related_functions.split(";") if self.research_question.related_functions is not None else ["-"],
            layout_configuration=self.layout_configuration, 
            links_register=self.links_register, 
            translator=self.translator)
        self._component_element = WrappedBulletListElement(
            max_width=self.layout_configuration.analysis_details_width,
            bullet_list=self.research_question.related_components.split(";") if self.research_question.related_components is not None else ["-"],
            layout_configuration=self.layout_configuration, 
            links_register=self.links_register, 
            translator=self.translator)
        
        w_titles_max = self.layout_configuration.small_margin + max([
            measure_text(self.translator.get_label(self.drivers_title), self.layout_configuration.font_size)[0],
            measure_text(self.translator.get_label(self.functions_title), self.layout_configuration.font_size)[0],
            measure_text(self.translator.get_label(self.components_title), self.layout_configuration.font_size)[0]
        ]) + self.layout_configuration.small_margin

        self._width = max(
            w_titles_max,
            self.layout_configuration.analysis_details_width,
        )

        self._height = (
            3 * (self.layout_configuration.small_margin
            + self.layout_configuration.font_size * 1.2
            + self.layout_configuration.small_margin)
            + self._driver_element.height
            + self._function_element.height
            + self._component_element.height
        )        
        return self

    @property
    def height(self) -> float:
        return self._height

    @property
    def width(self) -> float:
        return self._width

    def draw(self, dwg: Drawing, x: float, y: float):
        y_current = self.draw_bulleted_subsection(dwg=dwg, x=x, y=y + self.layout_configuration.small_margin, title=self.drivers_title, element=self._driver_element)
        y_current = self.draw_bulleted_subsection(dwg=dwg, x=x, y=y_current, title=self.functions_title, element=self._function_element)
        self.draw_bulleted_subsection(dwg=dwg, x=x, y=y_current, title=self.components_title, element=self._component_element)

    def draw_bulleted_subsection(self, dwg:Drawing, x: float, y: float, title: Label, element:WrappedBulletListElement) -> float:
        dwg.add(
            dwg.text(
                self.translator.get_label(title),
                insert=(
                    x + self.layout_configuration.small_margin,
                    y,
                ),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                font_style="italic",
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )
        y += self.layout_configuration.font_size * 1.2 + self.layout_configuration.small_margin
        self.draw_horizontal_separator(
            dwg=dwg, 
            x=x, 
            y=y, 
            element_width=self.width, 
            color=self.color)
        
        element.draw(
            dwg=dwg, 
            x=x, 
            y=y)
        
        y += element.height
        return y