from __future__ import annotations
from pydantic import model_validator
from svk.data._research_question import ResearchQuestion
from svk.data._research_line import ResearchLine
from svk.data._priority import Priority
from svk.data._timeframe import TimeFrame
from svk.data.helpers._greyfraction import color_toward_grey


class SluicesResearchQuestion(ResearchQuestion):
    prio_water_safety: Priority
    """Priority of this question related to water safety."""
    prio_water_availability: Priority
    """Priority of this question related to water availability."""
    prio_shipping: Priority
    """Priority of this question related to shipping."""
    prio_other_functions: Priority
    """Priority of this question related to functions of the barrier other than water safety."""
    prio_management_maintenance: Priority
    """Priority of this question related to maintenance of the barrier."""
    prio_operation: Priority
    """Priority of this question related to operation of the barrier."""
    sluice: str  # TODO: Make this an enum that can be translated to an icon?
    """The sluice this question is related to."""
    research_line: ResearchLine | None
    """The research line this question is associated with."""
    research_program: str | None = None
    """The research program this question is associated with."""
    status: str | None = None
    """The status of this question."""
    contributes_to_standardisation: bool
    """Indicates whether the answer to this question contributes to standardisation of sluices."""

    @model_validator(mode="after")
    def check_research_line(self) -> SluicesResearchQuestion:
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
            if sum(
                [
                    self.prio_water_safety.id,
                    self.prio_water_availability.id,
                    self.prio_shipping.id,
                    self.prio_other_functions.id,
                    self.prio_management_maintenance.id,
                    self.prio_operation.id,
                ]
            )
            > 8
            else 0
        )
