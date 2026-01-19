from pydantic import BaseModel, model_validator, Field
import math

from svk.data import ResearchQuestion
from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.helpers._drawwrappedtext import wrapped_text, wrapped_lines
from svk.visualization.helpers._greyfraction import color_toward_grey


def draw_priority_arrow(dwg, x: float, y: float, width: float, height: float = 5, stroke_color="black"):
    stroke_width = 3
    line1 = dwg.line(
        start=(x, y + height / 2),
        end=(x + width / 2, y - height / 2),
        stroke=stroke_color,
        stroke_width=stroke_width,
        stroke_linecap="round",
    )
    line2 = dwg.line(
        start=(x + width / 2, y - height / 2),
        end=(x + width, y + height / 2),
        stroke=stroke_color,
        stroke_width=stroke_width,
        stroke_linecap="round",
    )
    dwg.add(line1)
    dwg.add(line2)
    pass


class Question(BaseModel):
    research_question: ResearchQuestion
    max_width: int = 570  # TODO: Progress or derive
    font_size: int = 12
    text_margin: int = 5
    priority_width: int = 15
    height: int = Field(default_factory=int)
    _lines: list[str] = []

    @model_validator(mode="after")
    def compute_height(self):
        self._lines = wrapped_lines(
            self.research_question.question,
            max_width=self.max_width - self.text_margin - self.priority_box_width,
            font_size=self.font_size,
        )

        self.height = math.ceil(self.font_size * len(self._lines) * 1.2 + self.text_margin * 2.0)

        return self

    @property
    def high_priority(self) -> bool:
        return (
            self.research_question.prio_bando.id == 3
            or self.research_question.prio_water_safety.id == 3
            or self.research_question.prio_operation.id == 3
            or (
                self.research_question.prio_bando.id
                + self.research_question.prio_operation.id
                + self.research_question.prio_water_safety.id
                + self.research_question.prio_functions.id
            )
            > 8
        )

    @property
    def color(self):
        research_line = self.research_question.research_line_primary
        return color_toward_grey(
            research_line.base_color,
            self.research_question.time_frame.grey_fraction,
        )

    def draw(self, dwg, x, y):
        width = self.max_width

        question_color = color_toward_grey(
            self.research_question.research_line_primary.base_color, self.research_question.time_frame.grey_fraction
        )

        dwg.add(
            dwg.rect(
                insert=(x, y),
                size=(width, self.height),
                stroke_width=0.5,
                fill=question_color,
                fill_opacity=0.3,
                stroke=question_color,
            )
        )

        y_middle = y + self.height / 2
        if not self.high_priority:
            draw_priority_arrow(dwg, x=x + self.text_margin, y=y_middle, width=self.priority_width)
        else:
            draw_priority_arrow(dwg, x=x + self.text_margin, y=y_middle - 2.5, width=self.priority_width)
            draw_priority_arrow(dwg, x=x + self.text_margin, y=y_middle + 2.5, width=self.priority_width)
        # else:
        #     draw_priority_arrow(dwg, x=x + self.text_margin, y=y_middle + 5, width=self.priority_width)
        #     draw_priority_arrow(dwg, x=x + self.text_margin, y=y_middle, width=self.priority_width)
        #     draw_priority_arrow(dwg, x=x + self.text_margin, y=y_middle - 5, width=self.priority_width)

        if len(self._lines) < 1:
            self._lines = wrapped_lines(
                self.research_question.question,
                max_width=width - 2 * self.text_margin - self.priority_box_width,
                font_size=self.font_size,
            )

        dwg.add(
            wrapped_text(
                dwg,
                lines=self._lines,
                insert=(x + self.priority_box_width, y + self.text_margin),
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )

        pass

    @property
    def priority_box_width(self) -> int:
        return self.priority_width + self.text_margin + self.text_margin
