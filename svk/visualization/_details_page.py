from svk.visualization._question_details import QuestionDetails
from svk.visualization._visual_element import VisualElement
from svgwrite import Drawing


class DetailsPage(VisualElement):
    page_number: int
    title: str
    questions: list[QuestionDetails] = []

    def draw(self) -> Drawing:
        paper_height = (
            self.layout_configuration.paper_margin
            + self.layout_configuration.page_title_height
            + self.layout_configuration.element_margin
            + sum([q.height + self.layout_configuration.element_margin for q in self.questions])
            + self.layout_configuration.paper_margin
        )

        dwg = Drawing(size=(f"{self.layout_configuration.details_page_width}px", f"{paper_height}px"), debug=False)
        self.links_register.register_page(
            page_number=self.page_number, width=self.layout_configuration.details_page_width, height=paper_height
        )

        dwg.add(
            dwg.text(
                self.title,
                insert=(
                    self.layout_configuration.paper_margin,
                    self.layout_configuration.paper_margin + self.layout_configuration.page_title_height / 2,
                ),
                font_size=self.layout_configuration.page_title_font_size,
                font_family="Arial",
                font_weight="bold",
                text_anchor="start",
                dominant_baseline="middle",
            )
        )

        y_current = (
            self.layout_configuration.paper_margin + self.layout_configuration.page_title_height + self.layout_configuration.element_margin
        )
        for question in self.questions:
            self.links_register.register_link_target(
                link_target=question.research_question.id,
                page_number=self.page_number,
                x=self.layout_configuration.paper_margin,
                y=y_current,
            )
            question.draw(
                dwg=dwg,
                x=self.layout_configuration.paper_margin,
                y=y_current,
                width=self.layout_configuration.details_page_width - 2 * self.layout_configuration.paper_margin,
                page_number=self.page_number,
            )
            y_current += question.height + self.layout_configuration.element_margin

        return dwg
