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

from svk.visualization.elements._question_details import QuestionDetailsElement
from svk.visualization.pages._page import Page
from svgwrite import Drawing


class DetailsPage(Page):
    questions: list[QuestionDetailsElement] = []

    def get_content_size(self) -> tuple[float, float]:
        return (
            self.layout_configuration.details_page_width,
            sum([q.height + self.layout_configuration.intermediate_margin for q in self.questions])
            - self.layout_configuration.intermediate_margin,
        )

    def draw_content(self, dwg: Drawing, top: float, left: float):
        top_current = top
        for question in self.questions:
            self.links_register.register_link_target(
                link_target=question.research_question.id,
                page_number=self.page_number,
                x=self.layout_configuration.paper_margin,
                y=top_current,
            )
            question.draw(
                dwg=dwg,
                x=left,
                y=top_current,
                width=self.layout_configuration.details_page_width - 2 * self.layout_configuration.paper_margin,
                page_number=self.page_number,
            )
            top_current += question.height + self.layout_configuration.intermediate_margin

        return dwg
