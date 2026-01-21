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
from pydantic import BaseModel, model_validator

from svk.data._timeframe import TimeFrame
from svk.data._priority import Priority
from svk.data._researchline import ResearchLine


class ResearchQuestion(BaseModel):
    id: str
    question: str
    explanation: str | None = None
    storm_surge_barrier: list[str]
    reference_ids: list[str]
    reference_question: int | None = None

    prio_water_safety: Priority
    prio_other_functions: Priority
    prio_management_maintenance: Priority
    prio_operation: Priority

    time_frame: TimeFrame
    lead_time: float | None = None

    research_line_primary: ResearchLine | None
    research_line_secondary: ResearchLine | None = None

    action_holder: str | None = None
    costs_estimate: float | None = None

    @model_validator(mode="after")
    def check_research_line(cls, model):
        if model.time_frame not in (TimeFrame.NotRelevant, TimeFrame.Unknown) and model.research_line_primary is None:
            raise ValueError("Research line can only be unknown in case the time frame is either not relevant or unknown.")
        return model
