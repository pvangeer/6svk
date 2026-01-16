from pydantic import BaseModel, model_validator, Field
import math

from svk.data import ResearchQuestion
from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.helpers._drawwrappedtext import wrapped_text


class Question(BaseModel):
    research_question: ResearchQuestion
    max_width: int = 570  # TODO: Progress or derive
    font_size: int = 12
    text_margin: int = 5
    height: int = Field(default_factory=int)

    @model_validator(mode="after")
    def compute_height(self):
        (w, h) = measure_text(self.research_question.question, self.font_size)
        n_lines = math.ceil(w / (self.max_width - 2 * self.text_margin))
        self.height = math.ceil(h * n_lines * 1.2 + self.text_margin * 2.0)

        return self

    def draw(self, dwg, x, y):
        width = self.max_width

        dwg.add(dwg.rect(insert=(x, y), size=(width, self.height), stroke_width=0.5, fill="white", stroke="black"))
        dwg.add(
            wrapped_text(
                dwg,
                self.research_question.question,
                (x + self.text_margin, y + self.text_margin),
                max_width=width - 2 * self.text_margin,
                dominant_baseline="text-before-edge",
            )
        )

        pass
