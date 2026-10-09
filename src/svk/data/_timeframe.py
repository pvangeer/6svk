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
from svk.data._label import Label


class TimeFrame(Enum):
    """
    The time frame of a research question. The time frame is expressed as one of the following values:
    - NotRelevant (niet relevant)
    - Now (nu)
    - NearFuture (nabije toekomst)
    - Future (toekomst)
    - Unknown (onbekend)

    After initiation, the enum class has two properties that express:
    [description] - The description of the time frame in terms of a translatable label.
    """

    NotRelevant = Label.TFNotRelevant
    Now = Label.TFNow
    NearFuture = Label.TFNearFuture
    Future = Label.TFFuture
    Unknown = Label.TFUnknown

    def __init__(self, description: Label):
        self.description: Label = description
        """The Dutch description of the time frame."""
