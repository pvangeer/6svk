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

from svgwrite import Drawing
from svk.visualization._header import Header
from svk.visualization._group import Group
from svk.visualization._layout_configuration import LayoutConfiguration
from pydantic import BaseModel


class Column(BaseModel):
    """
    Class that represents a Column.
    """

    layout_configuration: LayoutConfiguration = LayoutConfiguration()
    """The layout configuration that is shared across the figures objects."""
    header_title: str
    """Header/title of the column"""
    header_sub_title: str
    """Subtitle of the columns header."""
    header_color: str
    """Color of the column (used as shading and as stroke color)"""
    groups: dict[int, Group] = {}
    """The groups that are part of this column"""
    y_color_groups: dict[int, float] = {}
    """Predefined start height of the various groups in the columns."""

    @property
    def header(self) -> Header:
        """
        The header object of the header of this column
        """
        return Header(title=self.header_title, sub_title=self.header_sub_title, color=self.header_color)

    def get_height(self, paper_header_height: float = 0):
        """
        Calculates the height of the column

        :param paper_header_height: Height of the paper header (needed in case y_color_groups is used.)
        :type paper_header_height: float
        """
        if not self.y_color_groups:
            return self.layout_configuration.column_header_height + sum(
                [group.get_height() + 2 * self.layout_configuration.element_margin for group in self.groups.values()]
            )

        max_group = max(self.groups.keys())
        return (
            self.y_color_groups[max_group]
            + self.groups[max_group].get_height()
            + 2 * self.layout_configuration.element_margin
            - paper_header_height
        )

    def draw(self, dwg: Drawing, x: float, y: float):
        """
        Draws the column on the svgwrite.Drawing.

        :param dwg: The svgwrite.Drawing object
        :type dwg: Drawing
        :param x: The x-position of the left upper corner of the column
        :type x: float
        :param y: The y-position of the left upper corner of the column
        :type y: float
        """
        self.header.draw(dwg, x, y)

        current_y = y + self.layout_configuration.column_header_height + 2 * self.layout_configuration.element_margin
        for i_group in sorted(self.groups.keys()):
            group = self.groups[i_group]
            if i_group in self.y_color_groups:
                current_y = self.y_color_groups[i_group]

            group.layout_configuration.arrow_depth = self.layout_configuration.arrow_depth
            group.draw(dwg, x, current_y, round(self.layout_configuration.column_width - self.layout_configuration.arrow_depth))

            current_y += group.get_height() + 2 * self.layout_configuration.element_margin
