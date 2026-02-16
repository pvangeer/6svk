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

from __future__ import annotations
from enum import Enum


class Priority(Enum):
    """
    The priority of a research question is an enum with a limited amount of possible values:
    0 - Unknown (onbekend)
    1 - Low (laag)
    2 - Medium (middel)
    3 - High (hoog)

    Above Description and id (number) are available through the properties "description" and "id" after initiation of the enum value.
    """

    High = (3, "hoog")
    Medium = (2, "middel")
    Low = (1, "laag")
    Unknown = (0, "onbekend")

    def __init__(self, id: int, description: str):
        self.description = description
        """The description of the priority value."""
        self.id = id
        """An int indicating the priority ranging from 0 - 3 (high number means high priority)."""
