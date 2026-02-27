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

from enum import Enum
from svk.data._translator import Label


class TimeFrame(Enum):
    """
    The time frame of a research question. The time frame is expressed as one of the following values:
    - NotRelevant (niet relevant)
    - Now (nu)
    - NearFuture (nabije toekomst)
    - Future (toekomst)
    - Unknown (onbekend)

    After initiation, the enum class has two properties that express:
    [description] - The Dutch description of the time frame.
    [grey_fraction] - The grey fraction associated to the specified time frame (a percentage expressed as a float between 0 and 1 that is used when generating colors during visualization)
    """

    NotRelevant = (Label.TFNotRelevant, 1)
    Now = (Label.TFNow, 0.0)
    NearFuture = (Label.TFNearFuture, 0.5)
    Future = (Label.TFFuture, 0.7)
    Unknown = (Label.TFUnknown, 0)

    def __init__(self, description: Label, grey_fraction: float):
        self.description: Label = description
        """The Dutch description of the time frame."""
        self.grey_fraction: float = grey_fraction
        """The grey fraction for this time frame (a percentage expressed as a float between 0 and 1)"""
