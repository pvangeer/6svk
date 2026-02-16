"""
Copyright (C) Stichting Deltares 2026. All rights reserved.

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

from pydantic import BaseModel, model_validator

from svk.data._timeframe import TimeFrame
from svk.data._priority import Priority
from svk.data._researchline import ResearchLine


class ResearchQuestion(BaseModel):
    """
    Data class representing a research question related to a storm surge barrier.
    """

    id: str
    """The unique id of the Question (represented with a string)."""
    question: str
    """The research question."""
    explanation: str | None = None
    """Further explanation of the research question."""
    storm_surge_barrier: list[str]  # TODO: Make this a list of StormSurgeBarrier objects
    """A list of storm surge barriers this question is related to."""
    reference_ids: list[str]
    """A list of id's of other research questions this question is related to."""
    reference_question: int | None = None
    """The number of this research question in the "160 questions list"."""

    prio_water_safety: Priority
    """Priority of this question related to water safety."""
    prio_other_functions: Priority
    """Priority of this question related to functions of the barrier other than water safety."""
    prio_management_maintenance: Priority
    """Priority of this question related to maintenance of the barrier."""
    prio_operation: Priority
    """Priority of this question related to operation of the barrier."""

    time_frame: TimeFrame
    """The time frame this question is associated with."""
    lead_time: float | None = None
    """The amount of time needed to come to an answer to the question in years."""

    research_line_primary: ResearchLine | None
    """The primary research line this question is associated with."""
    research_line_secondary: ResearchLine | None = None
    """An optional secondary research line this question is associated with."""

    action_holder: str | None = None
    """The organisation that is most likely to be responsible or leading in answering this research question."""
    costs_estimate: float | None = None
    """A first cost estimate for acquiring an answer to the research question."""

    @model_validator(mode="after")
    def check_research_line(cls, model):
        if model.time_frame not in (TimeFrame.NotRelevant, TimeFrame.Unknown) and model.research_line_primary is None:
            raise ValueError("Research line can only be unknown in case the time frame is either not relevant or unknown.")
        return model
