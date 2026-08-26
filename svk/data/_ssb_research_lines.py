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


class StormSurgeBarrierResearchLines(Enum):
    """
    This enum exposes default research line objects used in the SVK-project.
    """

    ConstructiveAspects = (1, Label.RL_ConstructiveAspects, 1)
    OperatingSystem = (2, Label.RL_OperatingSystem, 1)
    Facilities = (3, Label.RL_Facilities, 1)
    Maintenance = (4, Label.RL_Maintenance, 1)
    Cyber = (5, Label.RL_Cyber, 2)
    Hydrodynamics = (6, Label.RL_Hydrodynamics, 2)
    ProbabilityOfFailyre = (7, Label.RL_ProbabilityOfFailyre, 2)
    Adaptation = (8, Label.RL_Adaptation, 2)
    Organizational = (9, Label.RL_Organizational, 3)
    Lifespan = (10, Label.RL_Lifespan, 3)

    def __init__(self, number: int, title: Label, cluster: int):
        self.id: str = "#RL-" + str(number)
        self.number: int = number
        self.title: Label = title
        self.cluster: int = cluster
