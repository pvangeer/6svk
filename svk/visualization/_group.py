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
from svgwrite import Drawing
from svk.visualization._question import Question
from svk.visualization.helpers._draw_callout import draw_callout
from svk.visualization._layout_configuration import LayoutConfiguration


class Group(BaseModel):
    """
    A group of items (as part of a column)
    """

    layout_configuration: LayoutConfiguration = LayoutConfiguration()
    """The layour configuration shared across all figures' items"""
    title: str
    """The title of the group"""
    color: str
    """The color of the group"""
    questions: list[Question] = []
    """The questions in this group"""

    def get_height(self) -> float:
        """
        Calculates the height of the group in pixels

        :return: The height of the group
        :rtype: int
        """
        return (
            self.layout_configuration.group_header_height
            + sum([question.height + self.layout_configuration.line_margin for question in self.questions])
            + 2 * self.layout_configuration.line_margin
        )

    def draw(
        self, dwg: Drawing, x: float, y: float, width: float
    ):  # TODO: Should we pass width here, or should that be part of the layout_configuration?
        """
        Draws the group and its questions

        :param dwg: The svgwrite.Drawing object that should be used.
        :type dwg: Drawing
        :param x: The x-position of the left upper corner of the group
        :type x: float
        :param y: The y-position of the left upper corner of the group
        :type y: float
        :param width: The width of the group
        :type width: float
        """
        self.draw_header(dwg, x, y, width)

        current_y = y + self.layout_configuration.group_header_height + self.layout_configuration.line_margin
        for question in self.questions:
            # TODO: This is equal for all questions. Don't calculate here. Just derive
            question.layout_configuration.question_max_width = (
                width - self.layout_configuration.arrow_depth - 2 * self.layout_configuration.element_margin
            )
            question.draw(dwg, x + self.layout_configuration.arrow_depth + self.layout_configuration.element_margin, current_y)
            current_y += self.layout_configuration.line_margin + question.height
            pass

    def draw_header(self, dwg: Drawing, x: float, y: float, width: float):
        """
        Draws the groups header

        :param dwg: The svgwrite.Drawing object to use
        :type dwg: Drawing
        :param x: The x-position of the upper left corner of the header
        :type x: float
        :param y: The y-position of the upper left corner of the header
        :type y: float
        :param width: The width of the header
        :type width: float
        """
        draw_callout(dwg, x, y, width, self.get_height(), self.color)

        dwg.add(
            dwg.text(
                self.title,
                insert=(
                    x + self.layout_configuration.arrow_depth + self.layout_configuration.element_margin,
                    y + self.layout_configuration.group_header_height / 2,
                ),
                font_size=self.layout_configuration.group_title_font_size,
                font_family="Arial",
                font_weight="bold",
                text_anchor="start",
                dominant_baseline="middle",
            )
        )
