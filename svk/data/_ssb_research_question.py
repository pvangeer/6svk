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

from __future__ import annotations

from svk.data._priority import Priority
from svk.data._research_line import ResearchLine
from svk.data._research_question import ResearchQuestion
from svk.data._stormsurgebarrier import StormSurgeBarrier
from svk.data.helpers._greyfraction import color_toward_grey


class StormSurgeBarrierResearchQuestion(ResearchQuestion):
    reference_question: int | None = None
    """The number of this research question in the "160 questions list"."""

    storm_surge_barriers: list[StormSurgeBarrier]
    """A list of storm surge barriers this question is related to."""

    prio_water_safety: Priority
    """Priority of this question related to water safety."""
    prio_other_functions: Priority
    """Priority of this question related to functions of the barrier other than water safety."""
    prio_management_maintenance: Priority
    """Priority of this question related to maintenance of the barrier."""
    prio_operation: Priority
    """Priority of this question related to operation of the barrier."""
    prio_explanation: str | None = None

    lead_time: float | None = None
    """The amount of time needed to come to an answer to the question in years."""

    research_line_secondary: ResearchLine | None = None
    """An optional secondary research line this question is associated with."""
    # TODO: research line explanation

    action_holder: str | None = None
    """The organisation that is most likely to be responsible or leading in answering this research question."""
    costs_estimate: float | None = None
    """A first cost estimate for acquiring an answer to the research question."""

    related_drivers: str | None = None
    """The drivers related to this question."""
    related_functions: str | None = None
    """The functions related to this question."""
    related_components: str | None = None
    """The components related to this question."""

    @property
    def color(self) -> str:
        research_line = self.research_line
        return (
            color_toward_grey(
                research_line.base_color,
                self.time_frame.grey_fraction,
            )
            if research_line is not None
            else "rgb(120,120,120)"
        )

    @property
    def priority(self) -> int:
        return (
            1
            if (
                self.prio_management_maintenance.id == 3
                or self.prio_water_safety.id == 3
                or self.prio_operation.id == 3
                or (self.prio_management_maintenance.id + self.prio_operation.id + self.prio_water_safety.id + self.prio_other_functions.id)
                > 8
            )
            else 0
        )
