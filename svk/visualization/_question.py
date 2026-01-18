from pydantic import BaseModel, model_validator, Field
import math

from svk.data import ResearchQuestion
from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.helpers._drawwrappedtext import wrapped_text, wrapped_lines
from svk.visualization.helpers._greyfraction import color_toward_grey


class Question(BaseModel):
    research_question: ResearchQuestion
    max_width: int = 570  # TODO: Progress or derive
    font_size: int = 12
    text_margin: int = 5
    priority_width: int = 25
    height: int = Field(default_factory=int)

    @model_validator(mode="after")
    def compute_height(self):
        (w, h) = measure_text(self.research_question.question, self.font_size)
        n_lines = math.ceil(w / (self.max_width - 2 * self.text_margin - self._get_priority_box_width))
        self.height = math.ceil(h * n_lines * 1.2 + self.text_margin * 2.0)

        return self

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
        lines = wrapped_lines(
            self.research_question.question, max_width=width - 2 * self.text_margin - self._get_priority_box_width, font_size=self.font_size
        )
        dwg.add(
            wrapped_text(
                dwg,
                lines=lines,
                insert=(x + self.text_margin + 2 * self.text_margin + self.priority_width, y + self.text_margin),
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )

        pass

    @property
    def _get_priority_box_width(self) -> int:
        return self.priority_width + self.text_margin + self.text_margin
