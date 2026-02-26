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

from pydantic import BaseModel


class LayoutConfiguration(BaseModel):
    # Margins
    paper_margin: float = 20.0
    large_margin: float = 20.0
    intermediate_margin: float = 10.0
    small_margin: float = 5.0

    # Font sizes
    page_title_font_size: int = 64
    column_header_font_size: int = 18
    group_title_font_size: int = 14
    font_size: int = 12
    disclamer_font_size: int = 8

    # Sizes
    page_title_height: float = 80
    column_header_height: float = 60
    group_header_height: float = 30

    n_columns: int = 3
    details_page_width: float = 1500.0
    column_width: float = 650.0
    question_priority_box_width: float = 15.0
    question_id_box_width: float = 40.0
    arrow_depth: float = 20

    cluster_colors: dict[int, tuple[int, int, int]] = {}
    """A dictionary with group colors."""

    @property
    def overview_page_width(self):
        return 2 * self.paper_margin + self.n_columns * self.column_width
