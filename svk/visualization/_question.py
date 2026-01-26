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

from pydantic import BaseModel, model_validator, Field
import math

from svk.data import ResearchQuestion
from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.helpers._drawwrappedtext import wrapped_text, wrapped_lines
from svk.visualization.helpers._greyfraction import color_toward_grey
from svk.visualization.helpers._draw_priority_arrow import draw_priority_arrow


class Question(BaseModel):
    research_question: ResearchQuestion
    max_width: int = 570  # TODO: Progress or derive
    font_size: int = 12
    text_margin: int = 5
    priority_width: int = 15
    svk_icon_width: int = 24
    height: int = Field(default_factory=int)
    _lines: list[str] = []

    @model_validator(mode="after")
    def compute_height(self):
        self._lines = wrapped_lines(
            self.research_question.question,
            # max_width=self.max_width - 2 * self.text_margin - self.priority_box_width - self.svk_icon_width,
            max_width=self.max_width - self.text_margin - self.priority_box_width,
            font_size=self.font_size,
        )

        self.height = math.ceil(self.font_size * len(self._lines) * 1.2 + self.text_margin * 2.0)

        return self

    @property
    def high_priority(self) -> bool:
        return (
            self.research_question.prio_management_maintenance.id == 3
            or self.research_question.prio_water_safety.id == 3
            or self.research_question.prio_operation.id == 3
            or (
                self.research_question.prio_management_maintenance.id
                + self.research_question.prio_operation.id
                + self.research_question.prio_water_safety.id
                + self.research_question.prio_other_functions.id
            )
            > 8
        )

    @property
    def color(self):
        research_line = self.research_question.research_line_primary
        return (
            color_toward_grey(
                research_line.base_color,
                self.research_question.time_frame.grey_fraction,
            )
            if research_line is not None
            else "rgb(120,120,120)"
        )

    def draw(self, dwg, x, y):
        width = self.max_width

        dwg.add(
            dwg.rect(
                insert=(x, y),
                size=(width, self.height),
                stroke_width=0.5,
                fill=self.color,
                fill_opacity=0.3,
                stroke=self.color,
            )
        )

        y_middle = y + self.height / 2
        if not self.high_priority:
            draw_priority_arrow(dwg, x=x + self.text_margin, y=y_middle, width=self.priority_width)
        else:
            draw_priority_arrow(dwg, x=x + self.text_margin, y=y_middle - 2.5, width=self.priority_width)
            draw_priority_arrow(dwg, x=x + self.text_margin, y=y_middle + 2.5, width=self.priority_width)

        if len(self._lines) < 1:
            self._lines = wrapped_lines(
                self.research_question.question,
                max_width=width - 2 * self.text_margin - self.priority_box_width - self.svk_icon_width,
                font_size=self.font_size,
            )

        dwg.add(
            wrapped_text(
                dwg,
                lines=self._lines,
                insert=(x + self.priority_box_width, y + self.text_margin),
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )

        pass

    @property
    def priority_box_width(self) -> int:
        return self.priority_width + self.text_margin + self.text_margin
