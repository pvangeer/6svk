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

from enum import Enum


class TimeFrame(Enum):
    NotRelevant = ("niet relevant", 1)
    Now = ("nu", 0.0)
    NearFuture = ("boeggolf", 0.5)
    Future = ("toekomst", 0.7)
    Unknown = ("onbekend", 0)

    def __init__(self, description: str, grey_fraction: float):
        self.description = description
        self.grey_fraction = grey_fraction
