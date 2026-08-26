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

from svk.data._ssb_research_question import StormSurgeBarrierResearchQuestion
from svk.data._impactcategory import ImpactCategory
from svk.data._priority import Priority


class ImpactPathwayResearchQuestion(StormSurgeBarrierResearchQuestion):
    impact_category: ImpactCategory
    prio_urgency_decision_making: Priority

    @property
    def priority(self) -> int:
        prios = [
            self.prio_management_maintenance,
            self.prio_operation,
            self.prio_other_functions,
            self.prio_urgency_decision_making,
            self.prio_water_safety,
        ]
        combined_priority = sum([p.id for p in prios])
        n_high_prio = sum(1 for p in prios if p.id == 3)
        if n_high_prio > 1 or combined_priority > 10:
            return 2
        if n_high_prio > 0 or combined_priority > 8:
            return 1
        return 0
