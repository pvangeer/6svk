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
from svk.visualization.helpers._drawwrappedtext import wrapped_text, wrapped_lines
from svk.visualization.helpers._greyfraction import color_toward_grey
from svk.visualization.helpers._draw_priority_arrow import draw_priority_arrow
from svk.visualization._layout_configuration import LayoutConfiguration


# TODO: Create base model that includes layout_configuration, height and draw. This will
class Question(BaseModel):
    """
    Represents a question element (as part of  a group, column and the figure)
    """

    layout_configuration: LayoutConfiguration = LayoutConfiguration()
    """The layout configuration shared across all elements of a figure."""
    research_question: ResearchQuestion
    """The research question"""
    height: float = Field(default_factory=int)

    _lines: list[str] = []

    @model_validator(mode="after")
    def compute_height(self):
        self._lines = wrapped_lines(
            self.research_question.question,
            # max_width=self.max_width - 2 * self.text_margin - self.priority_box_width - self.svk_icon_width,
            max_width=self.layout_configuration.question_max_width - self.layout_configuration.line_margin - self._priority_box_width,
            font_size=self.layout_configuration.font_size,
        )

        self.height = self.layout_configuration.font_size * len(self._lines) * 1.2 + self.layout_configuration.line_margin * 2.0

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
    def _color(self):
        research_line = self.research_question.research_line_primary
        return (
            color_toward_grey(
                research_line.base_color,
                self.research_question.time_frame.grey_fraction,
            )
            if research_line is not None
            else "rgb(120,120,120)"
        )

    @property
    def _priority_box_width(self) -> float:
        return self.layout_configuration.priority_width + self.layout_configuration.line_margin + self.layout_configuration.line_margin

    def draw(self, dwg, x, y):
        width = self.layout_configuration.question_max_width

        dwg.add(
            dwg.rect(
                insert=(x, y),
                size=(width, self.height),
                stroke_width=0.5,
                fill=self._color,
                fill_opacity=0.3,
                stroke=self._color,
            )
        )

        y_middle = y + self.height / 2
        if not self.high_priority:
            draw_priority_arrow(
                dwg, x=x + self.layout_configuration.line_margin, y=y_middle, width=self.layout_configuration.priority_width
            )
        else:
            draw_priority_arrow(
                dwg, x=x + self.layout_configuration.line_margin, y=y_middle - 2.5, width=self.layout_configuration.priority_width
            )
            draw_priority_arrow(
                dwg, x=x + self.layout_configuration.line_margin, y=y_middle + 2.5, width=self.layout_configuration.priority_width
            )

        if len(self._lines) < 1:
            self._lines = wrapped_lines(
                self.research_question.question,
                max_width=width
                - 2 * self.layout_configuration.line_margin
                - self._priority_box_width
                - self.layout_configuration.svk_icon_width,
                font_size=self.layout_configuration.font_size,
            )

        dwg.add(
            wrapped_text(
                dwg,
                lines=self._lines,
                insert=(x + self._priority_box_width, y + self.layout_configuration.line_margin),
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )

        pass
