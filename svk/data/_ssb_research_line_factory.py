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
from svk.data._research_line import ResearchLine
from svk.data._ssb_research_lines import StormSurgeBarrierResearchLines

orange = (233, 113, 50)
light_green = (142, 178, 30)
dark_green = (25, 107, 36)


class StormSurgeBarrierResearchLineFactory(BaseModel):
    @staticmethod
    def get_ssb_research_line_from_int(number: int) -> StormSurgeBarrierResearchLines:
        match number:
            case 1:
                return StormSurgeBarrierResearchLines.ConstructiveAspects
            case 2:
                return StormSurgeBarrierResearchLines.OperatingSystem
            case 3:
                return StormSurgeBarrierResearchLines.Facilities
            case 4:
                return StormSurgeBarrierResearchLines.Maintenance
            case 5:
                return StormSurgeBarrierResearchLines.Cyber
            case 6:
                return StormSurgeBarrierResearchLines.Hydrodynamics
            case 7:
                return StormSurgeBarrierResearchLines.ProbabilityOfFailyre
            case 8:
                return StormSurgeBarrierResearchLines.Adaptation
            case 9:
                return StormSurgeBarrierResearchLines.Organizational
            case 10:
                return StormSurgeBarrierResearchLines.Lifespan
            case _:
                raise ValueError("Unknown research line")

    @staticmethod
    def get_research_line_from_int(number: int) -> ResearchLine:
        """
        This method returns a research line object associated to a particular research line number.

        :param number: The number associated to the desired research line.
        :type number: int
        :return: The associated research line.
        :rtype: ResearchLine
        """
        return StormSurgeBarrierResearchLineFactory.get_research_line_from_ssb_enum(
            StormSurgeBarrierResearchLineFactory.get_ssb_research_line_from_int(number)
        )

    @staticmethod
    def get_research_line_from_ssb_enum(storm_surge_barrier_research_line: StormSurgeBarrierResearchLines) -> ResearchLine:
        return ResearchLine(
            number=storm_surge_barrier_research_line.number,
            title=storm_surge_barrier_research_line.title,
            cluster=storm_surge_barrier_research_line.cluster,
            base_color=StormSurgeBarrierResearchLineFactory.get_base_color(storm_surge_barrier_research_line.cluster),
        )

    @staticmethod
    def get_base_color(cluster) -> tuple[int, int, int]:
        """
        Returns the R, G and B values of the color associated to the color group of the research line. R,G and B are integers ranging from 0 - 256.

        :return: R,G,B of the associated color.
        :rtype: tuple[int, int, int]
        """
        match cluster:
            case 1:
                return orange
            case 2:
                return light_green
            case 3:
                return dark_green
        raise ValueError("Unknown color group.")
