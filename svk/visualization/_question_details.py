from pydantic import Field, model_validator
from svk.data import ResearchQuestion
from svgwrite import Drawing
from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.helpers._drawwrappedtext import wrapped_text, wrapped_lines
from svk.visualization.helpers._greyfraction import color_toward_grey
from svk.visualization._visual_element import VisualElement
from svk.visualization.helpers._draw_priority_arrow import draw_priority_arrow


class QuestionDetails(VisualElement):
    research_question: ResearchQuestion
    """The research question"""

    height: float = Field(default_factory=int)
    w_code_field: float = Field(default_factory=float)
    w_relation_field: float = Field(default_factory=float)
    w_priority_field_fixed: float = Field(default_factory=float)
    w_priority_field: float = Field(default_factory=float)
    h_second_line: float = Field(default_factory=float)
    priority_explained_lines: list[str] = Field(default_factory=list[str])
    w_question_field: float = Field(default_factory=float)
    question_lines: list[str] = Field(default_factory=list[str])
    question_explained_lines: list[str] = Field(default_factory=list[str])

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
    def compute_dimensions(self):
        self.w_code_field = (
            max(
                self.layout_configuration.question_priority_box_width,
                self.layout_configuration.question_id_box_width,
            )
            + 2 * self.layout_configuration.element_margin
        )

        self.h_second_line = (
            self.layout_configuration.element_margin + self.layout_configuration.font_size + self.layout_configuration.element_margin
        )
        h_code_field = self.h_second_line + self.layout_configuration.question_priority_box_width + self.layout_configuration.element_margin
        self.w_relation_field = self.layout_configuration.question_id_box_width + self.layout_configuration.element_margin
        h_relation_field = (
            self.h_second_line
            + len(self.research_question.reference_ids) * self.layout_configuration.font_size * 1.2
            + self.layout_configuration.element_margin
        )
        self.w_priority_field_fixed = 50
        h_priority_fixed_field = self.h_second_line + 4 * self.layout_configuration.font_size * 1.2 + self.layout_configuration.line_margin
        w_remaining = self.layout_configuration.page_width - self.w_code_field - self.w_priority_field_fixed - self.w_relation_field
        self.w_priority_field = w_remaining * 0.4
        self.priority_explained_lines = []
        h_priority_field = (
            self.h_second_line
            + len(self.priority_explained_lines) * self.layout_configuration.font_size * 1.2
            + self.layout_configuration.element_margin
        )

        self.w_question_field = w_remaining * 0.6
        self.question_lines = wrapped_lines(
            self.research_question.question,
            self.w_question_field - 2 * self.layout_configuration.line_margin,
            self.layout_configuration.font_size,
        )
        self.question_explained_lines = wrapped_lines(
            str(self.research_question.explanation) if not None else "",
            self.w_question_field - 2 * self.layout_configuration.line_margin,
            self.layout_configuration.font_size,
        )
        h_question_field = (
            self.layout_configuration.element_margin
            + len(self.question_lines) * self.layout_configuration.font_size * 1.2
            + self.layout_configuration.element_margin
            + len(self.question_explained_lines) * self.layout_configuration.font_size * 1.2
            + self.layout_configuration.element_margin
        )

        self.height = max(h_code_field, h_priority_field, h_priority_fixed_field, h_question_field, h_relation_field)

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
                insert=(x + self.layout_configuration.element_margin, y + self.layout_configuration.element_margin),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )

        prio_height = (
            self.height
            - self.layout_configuration.element_margin
            - self.layout_configuration.line_margin
            - self.layout_configuration.font_size * 1.2
        )
        y_middle = (
            y
            + self.layout_configuration.element_margin
            + self.layout_configuration.line_margin
            + self.layout_configuration.font_size * 1.2
            + prio_height / 2.0
        )
        x_prio_left = x + self.w_code_field / 2 - self.layout_configuration.question_priority_box_width / 2
        if not self.research_question.has_priority:
            draw_priority_arrow(dwg, x=x_prio_left, y=y_middle, width=self.layout_configuration.question_priority_box_width)
        else:
            draw_priority_arrow(
                dwg,
                x=x_prio_left,
                y=y_middle - 2.5,
                width=self.layout_configuration.question_priority_box_width,
            )
            draw_priority_arrow(
                dwg,
                x=x_prio_left,
                y=y_middle + 2.5,
                width=self.layout_configuration.question_priority_box_width,
            )

        dwg.add(
            wrapped_text(
                dwg,
                self.question_lines,
                insert=(x + self.w_code_field, y + self.layout_configuration.element_margin),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )

        dwg.add(
            wrapped_text(
                dwg,
                self.question_explained_lines,
                insert=(
                    x + self.w_code_field,
                    y
                    + self.layout_configuration.element_margin
                    + len(self.question_lines) * self.layout_configuration.font_size * 1.2
                    + self.layout_configuration.element_margin,
                ),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )
