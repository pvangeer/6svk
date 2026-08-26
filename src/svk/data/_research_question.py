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
from pydantic import BaseModel, model_validator
from svk.data._timeframe import TimeFrame
from svk.data._research_line import ResearchLine
from abc import ABC, abstractmethod


class ResearchQuestion(ABC, BaseModel):
    """
    Data class representing a research question related to a storm surge barrier.
    """

    id: str
    """The unique id of the Question (represented with a string)."""
    question: str
    """The research question."""
    explanation: str | None = None
    """Further explanation of the research question."""

    reference_ids: list[str]
    """A list of id's of other research questions this question is related to."""

    time_frame: TimeFrame
    """The time frame this question is associated with."""
    # TODO: Time frame explanation

    research_line: ResearchLine | None
    """The primary research line this question is associated with."""

    keywords: str | None
    """Keywords associated with this research question. These keywords are used to search for research questions in the database."""

    @property
    @abstractmethod
    def color(self) -> str:
        pass

    @property
    @abstractmethod
    def priority(self) -> int:
        """
        Returns the priority of this research question. The priority is an integer between 0 and 2, where 0 is low priority, 1 is medium priority and 2 is high priority.

        :return: The priority of this research question.
        :rtype: int
        """
        pass

    @model_validator(mode="after")
    def check_research_line(self) -> ResearchQuestion:
        if self.time_frame not in (TimeFrame.NotRelevant, TimeFrame.Unknown) and self.research_line is None:
            raise ValueError("Research line can only be unknown in case the time frame is either not relevant or unknown.")
        return self
