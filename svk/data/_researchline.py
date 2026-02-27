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

orange = (233, 113, 50)
light_green = (142, 178, 30)
dark_green = (25, 107, 36)


class ResearchLine(Enum):
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
        self.number: int = number
        self.title: Label = title
        self.cluster: int = cluster

    @property
    def base_color(self) -> tuple[int, int, int]:
        """
        Returns the R, G and B values of the color associated to the color group of the research line. R,G and B are integers ranging from 0 - 256.

        :return: R,G,B of the associated color.
        :rtype: tuple[int, int, int]
        """
        match self.cluster:
            case 1:
                return orange
            case 2:
                return light_green
            case 3:
                return dark_green
        raise ValueError("Unknown color group.")


def get_research_line(number: int) -> ResearchLine:
    """
    This method returns a research line object associated to a particular research line number.

    :param number: The number associated to the desired research line.
    :type number: int
    :return: The associated research line.
    :rtype: ResearchLine
    """
    match number:
        case 1:
            return ResearchLine.ConstructiveAspects
        case 2:
            return ResearchLine.OperatingSystem
        case 3:
            return ResearchLine.Facilities
        case 4:
            return ResearchLine.Maintenance
        case 5:
            return ResearchLine.Cyber
        case 6:
            return ResearchLine.Hydrodynamics
        case 7:
            return ResearchLine.ProbabilityOfFailyre
        case 8:
            return ResearchLine.Adaptation
        case 9:
            return ResearchLine.Organizational
        case 10:
            return ResearchLine.Lifespan
        case _:
            raise ValueError("Unknown research line")
