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

from pydantic import BaseModel, ConfigDict
from enum import Enum

orange = (233, 113, 50)
light_green = (142, 178, 30)
dark_green = (25, 107, 36)


class ResearchLine(BaseModel):
    """
    Data class representing a research line.
    """

    number: int
    """An integer associated to the particular research line."""
    title: str
    """The title of the research line."""
    cluster: int
    """The color group that is associated to the research line. This allows grouping of questions in different research lines visually by means of the same background color."""

    model_config = ConfigDict(frozen=True)

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
            return ResearchLines.ConstructiveAspects.value
        case 2:
            return ResearchLines.OperatingSystem.value
        case 3:
            return ResearchLines.Facilities.value
        case 4:
            return ResearchLines.Maintenance.value
        case 5:
            return ResearchLines.Cyber.value
        case 6:
            return ResearchLines.Hydrodynamics.value
        case 7:
            return ResearchLines.ProbabilityOfFailyre.value
        case 8:
            return ResearchLines.Adaptation.value
        case 9:
            return ResearchLines.Organizational.value
        case 10:
            return ResearchLines.Lifespan.value
        case _:
            raise ValueError("Unknown research line")


class ResearchLines(Enum):
    """
    This enum exposes default research line objects used in the SVK-project.
    """

    ConstructiveAspects = ResearchLine(number=1, title="Constructieve aspecten", cluster=1)
    OperatingSystem = ResearchLine(number=2, title="Besturingssystemen / IA", cluster=1)
    Facilities = ResearchLine(number=3, title="Voorzieningen en gebouwen", cluster=1)
    Maintenance = ResearchLine(number=4, title="Onderhoud en operatie", cluster=1)
    Cyber = ResearchLine(number=5, title="Cyber & security", cluster=2)
    Hydrodynamics = ResearchLine(number=6, title="Hydrodynamische effecten en belastingen", cluster=2)
    ProbabilityOfFailyre = ResearchLine(number=7, title="Faalkans", cluster=2)
    Adaptation = ResearchLine(number=8, title="Adaptatie stormvloedkeringen", cluster=2)
    Organizational = ResearchLine(number=9, title="Organisatorische aspecten", cluster=3)
    Lifespan = ResearchLine(number=10, title="Restlevensduur huidige objecten", cluster=3)
