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

from svk.visualization._header import Header
from svk.visualization._visual_element import VisualElement


class Column(VisualElement):
    """
    Class that represents a Column.
    """

    header_title: str
    """Header/title of the column"""
    header_subtitle: str
    """Subtitle of the columns header."""
    header_color: str
    """Color of the column (used as shading and as stroke color)"""
    number: int

    @property
    def header(self) -> Header:
        """
        The header object of the header of this column
        """
        return Header(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            title=self.header_title,
            subtitle=self.header_subtitle,
            color=self.header_color,
        )
