from __future__ import annotations

from pydantic import model_validator

from svk.data._priority import Priority
from svk.data._research_line import ResearchLine
from svk.data._research_question import ResearchQuestion
from svk.data._stormsurgebarrier import StormSurgeBarrier
from svk.data._timeframe import TimeFrame
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

    @model_validator(mode="after")
    def check_research_line(self) -> StormSurgeBarrierResearchQuestion:
        if self.time_frame not in (TimeFrame.NotRelevant, TimeFrame.Unknown) and self.research_line is None:
            raise ValueError("Research line can only be unknown in case the time frame is either not relevant or unknown.")
        return self

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
