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


class LinksRegister(BaseModel):
    links: dict[str, list[tuple[int, float, float, float, float]]] = {}
    """id, list[tuple[page_number, x, y, w, h]]"""
    link_targets: dict[str, tuple[int, float, float]] = {}
    """id, tuple[page_number, x, y]"""
    page_sizes: dict[int, tuple[float, float]] = {}
    """page_number, tuple[w, h]"""

    def register_link(self, link_target: str, page_number: int, x: float, y: float, width: float, height: float):
        if not link_target in self.links.keys():
            self.links[link_target] = []

        self.links[link_target].append((page_number, x, y, width, height))

    def register_link_target(self, link_target: str, page_number: int, x: float, y: float):
        self.link_targets[link_target] = (page_number, x, y)

    def register_page(self, page_number: int, width: float, height: float):
        self.page_sizes[page_number] = (width, height)
