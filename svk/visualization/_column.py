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
    groups: list[Group] = []
    column_width: int = 650
    group_margin: int = 20
    y_group_1: int | None = None
    y_group_2: int | None = None
    y_group_3: int | None = None

    @property
    def header(self) -> Header:
        return Header(title=self.header_title, sub_title=self.header_sub_title, color=self.header_color)

    def get_width(self):
        return self.column_width

    def get_height(self):
        if self.y_group_3 is not None:
            return self.y_group_3 + sum([group.get_height() + self.group_margin for group in self.groups if group.number == 3])
        elif self.y_group_2 is not None:
            return self.y_group_2 + sum([group.get_height() + self.group_margin for group in self.groups if group.number > 1])
        else:
            return self.header.height + sum([group.get_height() + self.group_margin for group in self.groups])

    def draw(self, dwg: Drawing, x: int, y: int):
        self.header.draw(dwg, x, y)

        current_y = y + self.header.height + self.group_margin
        current_group_no = self.groups[0] if self.groups else 1
        for group in self.groups:
            if current_group_no != group.number:
                current_group_no = group.number
                y_new = self.y_group_1 if group.number == 1 else self.y_group_2 if group.number == 2 else self.y_group_3
                if y_new is not None:
                    current_y = y_new

            group.arrow_depth = self.header.arrow_depth
            group.draw(dwg, x, current_y, round(self.column_width - self.header.arrow_depth))
            current_y += group.get_height() + self.group_margin
