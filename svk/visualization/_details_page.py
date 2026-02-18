from svk.visualization._question_details import QuestionDetails
from svk.visualization._visual_element import VisualElement
from svgwrite import Drawing


class DetailsPage(VisualElement):
    page_number: int
    questions: list[QuestionDetails] = []

    def draw(self) -> Drawing:
        paper_height = (
            sum([q.height + self.layout_configuration.element_margin for q in self.questions])
            + self.layout_configuration.paper_margin * 2
            - self.layout_configuration.element_margin
        )
        dwg = Drawing(size=(f"{self.layout_configuration.details_page_width}px", f"{paper_height}px"), debug=False)
        self.links_register.register_page(
            page_number=self.page_number, width=self.layout_configuration.details_page_width, height=paper_height
        )

        y = self.layout_configuration.paper_margin
        for question in self.questions:
            self.links_register.register_link_target(
                link_target=question.research_question.id, page_number=self.page_number, x=self.layout_configuration.paper_margin, y=y
            )
            question.draw(
                dwg,
                self.layout_configuration.paper_margin,
                y,
                self.layout_configuration.details_page_width - 2 * self.layout_configuration.paper_margin,
            )
            y += question.height + self.layout_configuration.element_margin

        return dwg
