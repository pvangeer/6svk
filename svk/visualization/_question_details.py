from pydantic import Field, model_validator
from svk.data import ResearchQuestion
from svgwrite import Drawing
from svk.visualization.helpers._drawwrappedtext import wrapped_text, wrapped_lines
from svk.visualization.helpers._greyfraction import color_toward_grey
from svk.visualization._visual_element import VisualElement


class QuestionDetails(VisualElement):
    research_question: ResearchQuestion
    """The research question"""
    height: float = Field(default_factory=int)

    def construct_lines(self):
        self._lines = wrapped_lines(
            self.research_question.question,
            max_width=self.layout_configuration.page_width
            - self.layout_configuration.paper_margin * 2
            - self.layout_configuration.question_id_box_width
            - 2 * self.layout_configuration.line_margin,
            font_size=self.layout_configuration.font_size,
        )

    @model_validator(mode="after")
    def compute_height(self):
        self.construct_lines()
        self.height = self.layout_configuration.font_size * len(self._lines) * 1.2 + self.layout_configuration.line_margin * 2.0

        return self

    @property
    def _color(self):
        research_line = self.research_question.research_line_primary
        return (
            color_toward_grey(
                research_line.base_color,
                self.research_question.time_frame.grey_fraction,
            )
            if research_line is not None
            else "rgb(120,120,120)"
        )

    def draw(self, dwg: Drawing, x: float, y: float, width: float):
        dwg.add(
            dwg.rect(
                insert=(x, y),
                size=(width, self.height),
                stroke_width=0.5,
                fill=self._color,
                fill_opacity=0.3,
                stroke=self._color,
            )
        )

        dwg.add(
            dwg.text(
                self.research_question.id,
                insert=(x + self.layout_configuration.element_margin, y + self.height / 2),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                text_anchor="start",
                dominant_baseline="middle",
                id=self.research_question.id,
            )
        )
