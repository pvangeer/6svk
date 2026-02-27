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


class StormSurgeBarrier(Enum):
    """
    Enum that represents one of the six storm surge barriers (or all of them together):
    - All ("6SVK")
    - MaeslantBarrier ("Maeslantkering")
    - HartelBarrier ("Hartelkering")
    - Ramspol ("Ramspol")
    - HollandseIJsselBarrier ("Hollandsche IJssel Kering")
    - EasternScheldBarrier ("Oosterscheldekering")
    - HaringvlietBarrier ("Haringvlietsluizen")

    After initiation, the "title" property will containg the Dutch title of the storm surge barrier.
    """

    All = Label.SSB_All
    MaeslantBarrier = Label.SSB_MaeslantBarrier
    HartelBarrier = Label.SSB_HartelBarrier
    Ramspol = Label.SSB_Ramspol
    HollandseIJsselBarrier = Label.SSB_HollandseIJsselBarrier
    EasternScheldBarrier = Label.SSB_EasternScheldBarrier
    HaringvlietBarrier = Label.SSB_HaringvlietBarrier

    def __init__(self, title: Label):
        self.title: Label = title
        """The name of the storm surge barrier in Dutch."""
