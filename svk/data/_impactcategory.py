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


class ImpactCategory(Enum):
    """
    Enum that lists the impact categories. Labels do not have to be translated as they are only used in en-context.
    """

    SocioEconomicAndEnvironment = (
        1,
        "SSBs contribute to satisfying socio-economic and environmental needs in the hinterland",
        "The storm surge barriers contribute to satisfying the socio-economic and environmental needs in the hinterland. This implies that people, knowledge, data, and tools are available to determine what thehinterland requires from the storm surge barrier. These requirements will likely evolve over time due to changes in sea-level as well as changes in society.",
    )
    ReliableSSB = (
        2,
        "Reliable SSBs in technically good condition",
        "The storm surge barrier is reliable and in a good technical condition. The barrier is properly monitored and methods are available to determine the technical condition. Methods like an adaptive maintenance planning and people are available for timely decisions on maintenance and reinforcement of (parts of) the storm surge barrier in relation to the needs from the hinterland.",
    )
    MaintenanceDecisions = (
        3,
        "Well-balanced maintenance and end-of-life decisions for the SSBs by including the system, technical and economical perspective.",
        "A well-balanced maintenance is enabled and end-of-lifetime decision for the storm surge barriers can be made by including the system, technical and economical perspective. A time-based adaptive pathway is available to determine when a storm surge barrier reaches its end of life (functional and structural) and what the options and impacts are for maintenance, removal, replacement, closure. Supporting near-future decision making and avoiding maladaptation.",
    )
    HumanCapical = (
        4,
        "Human capital for a safe and liveable delta",
        "Human capital for a safe and liveable delta. There is a knowledgeable community of professionals that is enabled to cope with the challenges in deltas.",
    )
    Example = (
        5,
        "The Dutch Delta is an example how to deal with climate change in low-lying delta countries and the Dutch water sector remains a frontrunner",
        "The Dutch Delta is an example how to deal with climate change in low-lying delta-countries and the Dutch Water sector remains a frontrunner. Knowledge and experience are shared in an inclusive international community with organizations and countries facing similar climate challenges.",
    )

    def __init__(self, number: int, title: str, description: str):
        self.number = number
        """The number of the impact category."""
        self.title = title
        """The title of the impact categorie"""
        self.description = description
        """The description of the impact category"""
