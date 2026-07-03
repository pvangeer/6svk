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
from svk.visualization.elements._title_element import TitleElement
from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.helpers._wrappedtext import wrapped_lines, wrapped_text
from svk.visualization.elements._wrapped_bullet_list import WrappedBulletListElement
from svk.visualization.elements._visual_elements_container import VisualElementsContainer


class QuestionAnalysisDetailsElement(VisualElementsContainer):
    research_question: ResearchQuestion
    """The research question"""
    color: str
    page_number: int
    
    _driver_lines: list[str] = PrivateAttr()
    _function_lines: list[str] = PrivateAttr()
    _component_lines: list[str] = PrivateAttr()
    _driver_title_element: TitleElement = PrivateAttr()
    _function_title_element: TitleElement = PrivateAttr()
    _component_title_element: TitleElement = PrivateAttr()
    _driver_element: WrappedBulletListElement = PrivateAttr()
    _function_element: WrappedBulletListElement = PrivateAttr()
    _component_element: WrappedBulletListElement = PrivateAttr()

    _height: float = PrivateAttr()
    _width: float = PrivateAttr()

    @model_validator(mode="after")
    def validate(self) -> QuestionAnalysisDetailsElement:
        self._driver_title_element = TitleElement(
            title=Label.QD_Drivers,
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator
        )
        self._function_title_element = TitleElement(
            title=Label.QD_Functions,
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator
        )
        self._component_title_element = TitleElement(
            title=Label.QD_Components,
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator
        )
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
        
        self._width = max(
            self._driver_title_element.width,
            self._function_title_element.width,
            self._component_title_element.width,
            self.layout_configuration.analysis_details_width,
        )

        self._height = (
            self._driver_title_element.height
            + self._driver_element.height
            + self._function_title_element.height
            + self._function_element.height
            + self._component_title_element.height
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
        y_current = self.draw_bulleted_subsection(dwg=dwg, x=x, y=y + self.layout_configuration.small_margin, title_element=self._driver_title_element, element=self._driver_element)
        y_current = self.draw_bulleted_subsection(dwg=dwg, x=x, y=y_current, title_element=self._function_title_element, element=self._function_element)
        self.draw_bulleted_subsection(dwg=dwg, x=x, y=y_current, title_element=self._component_title_element, element=self._component_element)

    def draw_bulleted_subsection(self, dwg:Drawing, x: float, y: float, title_element: TitleElement, element:WrappedBulletListElement) -> float:
        title_element.draw(
            dwg=dwg,
            x=x,
            y=y - self.layout_configuration.small_margin
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