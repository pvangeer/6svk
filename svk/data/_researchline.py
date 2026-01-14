"""
Copyright (C) Stichting Deltares 2023-2024. All rights reserved.

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
from pydantic import BaseModel

from enum import Enum


class ResearchLine(BaseModel):
    number: int
    title: str

    @staticmethod
    def get_research_line(number: int) -> ResearchLine:
        match number:
            case 1:
                return ResearchLines.ConstructiveAspects.value
            case 2:
                return ResearchLines.OperatingSystem.value
            case 3:
                return ResearchLines.OperatingSystem.value
            case 4:
                return ResearchLines.OperatingSystem.value
            case 5:
                return ResearchLines.OperatingSystem.value
            case 6:
                return ResearchLines.OperatingSystem.value
            case 7:
                return ResearchLines.OperatingSystem.value
            case 8:
                return ResearchLines.OperatingSystem.value
            case 9:
                return ResearchLines.OperatingSystem.value
            case 10:
                return ResearchLines.OperatingSystem.value
            case _:
                raise ValueError("Unknown research line")


class ResearchLines(Enum):
    ConstructiveAspects = ResearchLine(number=1, title="Constructieve aspecten")
    OperatingSystem = ResearchLine(number=2, title="Besturingssystemen / IA")
    Facilities = ResearchLine(number=3, title="Voorzieningen en gebouwen")
    Maintenance = ResearchLine(number=4, title="Onderhoud (operationele aspecten)")
    Cyber = ResearchLine(number=5, title="Cyber & security")
    Hydrodynamics = ResearchLine(number=6, title="Hydrodynamische effecten en belastingen")
    ProbabilityOfFailyre = ResearchLine(number=7, title="Faalkans")
    Adaptation = ResearchLine(number=8, title="Adaptatie stormvloedkeringen")
    Organizational = ResearchLine(number=9, title="Organisatorische aspecten")
    Lifespan = ResearchLine(number=10, title="Restlevensduur huidige objecten")
