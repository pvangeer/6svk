from svk.visualization._question_details import QuestionDetails
from svk.visualization._visual_element import VisualElement
from svgwrite import Drawing


class DetailsPage(VisualElement):

    questions: list[QuestionDetails] = []

    def draw(self) -> Drawing:
        paper_height = (
            sum([q.height + self.layout_configuration.element_margin for q in self.questions])
            + self.layout_configuration.paper_margin * 2
            - self.layout_configuration.element_margin
        )
        dwg = Drawing(size=(f"{self.layout_configuration.page_width}px", f"{paper_height}px"), debug=False)
        # TODO: this should not be hardcoded 1.
        self.layout_configuration.page_sizes[1] = (self.layout_configuration.page_width, paper_height)

        y = self.layout_configuration.paper_margin
        for question in self.questions:
            self.layout_configuration.register_link_target(
                link_target=question.research_question.id, page_number=1, x=self.layout_configuration.paper_margin, y=y
            )
            question.draw(
                dwg,
                self.layout_configuration.paper_margin,
                y,
                self.layout_configuration.page_width - 2 * self.layout_configuration.paper_margin,
            )
            y += question.height + self.layout_configuration.element_margin

        return dwg
