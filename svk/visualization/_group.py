from svk.data import ResearchLine, ResearchQuestion
from svk.visualization._timeframeaware import TimeFrameAware
from svk.visualization._question import Question
from svk.visualization.helpers._greyfraction import color_toward_grey
from svk.visualization.helpers._drawwrappedtext import wrapped_text
import uuid


class Group(TimeFrameAware):
    research_line: ResearchLine
    questions: list[Question] = []
    base_color: tuple[int, int, int]

    header_height: int = 30
    header_margin: int = 10
    font_size: int = 14
    question_margin: int = 5
    arrow_depth: int = 20  # TODO: Progress

    @property
    def color(self):
        return color_toward_grey(self.base_color[0], self.base_color[1], self.base_color[2], self.grey_fraction())

    def get_height(self) -> int:
        return self.header_height + sum([question.height + self.question_margin for question in self.questions]) + self.question_margin

    def draw(self, dwg, x, y, width):
        self.draw_header(dwg, x, y, width)
        current_y = y + self.header_height + self.question_margin
        for question in self.questions:
            question.max_width = width - self.arrow_depth - 20
            question.draw(dwg, x + self.arrow_depth + 10, current_y)
            current_y += question.text_margin + question.height
            pass

    def draw_header(self, dwg, x, y, width):
        gradient_id = f"gradient_group_header_{str(uuid.uuid4())}"
        header_size = 30
        group_height = self.get_height()
        x_scale = width / header_size
        radial_grad = dwg.radialGradient(
            center=((x + 20) / x_scale, y),  # center in relative coords
            r=header_size,  # radius relative to box
            gradientUnits="userSpaceOnUse",
            id=gradient_id,
        )
        radial_grad.add_stop_color(0, self.color)  # center
        radial_grad.add_stop_color(1, "white")  # edge

        radial_grad["gradientTransform"] = f"scale({x_scale},1)"

        dwg.defs.add(radial_grad)

        points = [
            (x, y),
            (x + width, y),
            (x + width, y + group_height),
            (x + self.arrow_depth, y + group_height),
            (x + self.arrow_depth, y + self.header_height),
        ]

        polygon = dwg.polygon(points=points, stroke=self.color, fill=f"url(#{gradient_id})", stroke_width=0.5, id=str(uuid.uuid4()))
        dwg.add(polygon)

        dwg.add(
            wrapped_text(
                dwg,
                self.research_line.title,
                insert=(x + self.arrow_depth + self.header_margin, y + self.header_margin + self.font_size),
                max_width=width,
                font_size=self.font_size,
                font_weight="bold",
            )
        )
