from svk.visualization._question_details import QuestionDetails
from svk.visualization._page import Page
from svgwrite import Drawing


class DetailsPage(Page):
    questions: list[QuestionDetails] = []

    def get_content_size(self) -> tuple[float, float]:
        return (
            self.layout_configuration.details_page_width,
            sum([q.height + self.layout_configuration.intermediate_margin for q in self.questions])
            - self.layout_configuration.intermediate_margin,
        )

    def draw_content(self, dwg: Drawing, top: float, left: float):
        top_current = top
        for question in self.questions:
            self.links_register.register_link_target(
                link_target=question.research_question.id,
                page_number=self.page_number,
                x=self.layout_configuration.paper_margin,
                y=top_current,
            )
            question.draw(
                dwg=dwg,
                x=left,
                y=top_current,
                width=self.layout_configuration.details_page_width - 2 * self.layout_configuration.paper_margin,
                page_number=self.page_number,
            )
            top_current += question.height + self.layout_configuration.intermediate_margin

        return dwg
