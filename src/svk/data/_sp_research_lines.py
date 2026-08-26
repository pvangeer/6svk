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


class SluicesResearchLines(Enum):
    """
    This enum exposes default research line objects used in the Panheel sluice-project.
    """

    TechnicalLifeTimeCivilParts = (1, Label.RL_TechnicalLifeTimeCivilParts, 1)
    TechnicalLifeTimeInstallations = (2, Label.RL_TechnicalLifeTimeInstallations, 1)
    InspectionsMonitoringAndData = (3, Label.RL_InspectionsMonitoringAndData, 1)
    WaterSafety = (4, Label.RL_WaterSafety, 2)
    WaterSystemAndAvailability = (5, Label.RL_WaterSystemAndAvailability, 2)
    EcologyAndWaterQuality = (6, Label.RL_EcologyAndWaterQuality, 2)
    Functions = (7, Label.RL_Functions, 2)
    Operation = (8, Label.RL_Operation, 2)
    Robustness = (9, Label.RL_Robuustness, 2)
    Strategy = (10, Label.RL_Strategy, 2)
    EnvironmentalImpact = (11, Label.RL_EnvironmentalImpact, 2)
    Organizational = (12, Label.RL_SP_Organizational, 3)

    def __init__(self, number: int, title: Label, cluster: int):
        self.id: str = "#RL-" + str(number)
        self.number: int = number
        self.title: Label = title
        self.cluster: int = cluster
