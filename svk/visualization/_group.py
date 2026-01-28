"""
Copyright (C) Stichting Deltares 2026. All rights reserved.

This file is part of the dikernel-python toolbox.

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

from pydantic import BaseModel
from svk.visualization._question import Question
from svk.visualization.helpers._draw_callout import draw_callout


class Group(BaseModel):
    title: str
    color: str
    number: int
    questions: list[Question] = []

    header_height: int = 30
    header_margin: int = 10
    font_size: int = 14
    question_margin: int = 5
    arrow_depth: int = 20  # TODO: Progress

    def get_height(self) -> int:
        return self.header_height + sum([question.height + self.question_margin for question in self.questions]) + self.question_margin

    def draw(self, dwg, x, y, width):
        self.draw_header(dwg, x, y, width)
        current_y = y + self.header_height + self.question_margin
        for question in self.questions:
            question.max_width = width - self.arrow_depth - 20
            question.draw(dwg, x + self.arrow_depth + 10, current_y)
            current_y += question.text_margin + question.height
            pass

    def draw_header(self, dwg, x, y, width):
        draw_callout(dwg, x, y, width, self.get_height(), self.color)

        dwg.add(
            dwg.text(
                self.title,
                insert=(x + self.arrow_depth + self.header_margin, y + self.header_height / 2),
                font_size=self.font_size,
                font_family="Arial",
                font_weight="bold",
                text_anchor="start",
                dominant_baseline="middle",
            )
        )
