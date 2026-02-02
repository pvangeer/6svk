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
from pydantic import BaseModel


class Column(BaseModel):
    header_title: str
    header_sub_title: str
    header_color: str
    groups: dict[int, Group] = {}
    y_groups: dict[int, float] = {}
    column_width: int = 650
    group_margin: int = 20

    @property
    def header(self) -> Header:
        return Header(title=self.header_title, sub_title=self.header_sub_title, color=self.header_color)

    def get_width(self):
        return self.column_width

    def get_height(self, paper_header_height: float = 0):
        if not self.y_groups:
            return self.header.height + sum([group.get_height() + self.group_margin for group in self.groups.values()])

        max_group = max(self.groups.keys())
        return self.y_groups[max_group] + self.groups[max_group].get_height() + self.group_margin - paper_header_height

    def draw(self, dwg: Drawing, x: int, y: int):
        self.header.draw(dwg, x, y)

        current_y = y + self.header.height + self.group_margin
        for i_group in sorted(self.groups.keys()):
            group = self.groups[i_group]
            if i_group in self.y_groups:
                current_y = self.y_groups[i_group]

            group.arrow_depth = self.header.arrow_depth
            group.draw(dwg, x, current_y, round(self.column_width - self.header.arrow_depth))

            current_y += group.get_height() + self.group_margin
