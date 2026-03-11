import os
from pydantic import BaseModel
from abc import ABC, abstractmethod
from collections import defaultdict
from svk.data import ResearchQuestion, LinksRegister, ResearchLine, Translator, TimeFrame
from svk.io import svg_to_pdf_chrome, merge_pdf_files, add_links
from svk.visualization.helpers import _calendar_helper as helper
from svk.visualization._layout_configuration import LayoutConfiguration
from svk.visualization._overview_page import OverviewPage
from svk.visualization._details_page import DetailsPage
from svk.visualization._question_details import QuestionDetails
from svk.visualization._column import Column


class MainVisualizationContainer(BaseModel, ABC):
    layout_configuration: LayoutConfiguration = LayoutConfiguration()
    links_register: LinksRegister = LinksRegister()
    translator: Translator = Translator(lang="nl")
    questions: list[ResearchQuestion]
    output_dir: str
    output_file: str
    cleanup: bool = True
    """When set to false, intermediate files are left in the output dir."""

    @abstractmethod
    def create_overview_page(self, page_number: int) -> OverviewPage:
        pass

    def build(self):
        # build overview page
        overview = self.create_overview_page(page_number=0)

        # build detailed pages
        grouped_questions: defaultdict[ResearchLine, list[ResearchQuestion]] = defaultdict(list[ResearchQuestion])
        non_grouped: list[ResearchQuestion] = []
        for question in self.questions:
            if question.research_line_primary is None:
                non_grouped.append(question)
            else:
                grouped_questions[question.research_line_primary].append(question)

        details_pages: dict[ResearchLine, DetailsPage] = {}
        page_number = 1
        for research_line in sorted(grouped_questions, key=lambda r_l: r_l.number):
            details_pages[research_line] = self.create_details_page(
                page_number=page_number,
                title=str(research_line.number) + ". " + self.translator.get_label(research_line.title),
                link_target=research_line.id,
                questions=grouped_questions[research_line],
            )
            page_number += 1

        if len(non_grouped) > 0:
            uncategorized_page = self.create_details_page(
                page_number=page_number,
                title="Zonder onderzoekslijn",
                link_target="",
                questions=non_grouped,
            )

        # convert all to pdf
        overview_file_path = os.path.join(self.output_dir, self.output_file + " - overview.pdf")
        details_file_path_base = os.path.join(self.output_dir, self.output_file + " - details - ")
        svg_to_pdf_chrome(svg_dwg=overview.draw(), pdf_path=overview_file_path)
        detailed_pages_files: list[str] = []
        for r_l in details_pages:
            details_file_name = details_file_path_base + r_l.name + ".pdf"
            detailed_pages_files.append(details_file_name)
            svg_to_pdf_chrome(svg_dwg=details_pages[r_l].draw(), pdf_path=details_file_name)
        if len(non_grouped) > 0:
            uncategorized_file_name = details_file_path_base + "no-research-line.pdf"
            detailed_pages_files.append(uncategorized_file_name)
            svg_to_pdf_chrome(svg_dwg=uncategorized_page.draw(), pdf_path=uncategorized_file_name)

        no_links_output_file = os.path.join(self.output_dir, self.output_file + " - no links.pdf")
        merge_pdf_files([overview_file_path] + detailed_pages_files, no_links_output_file)

        # create links
        output_file_final = os.path.join(self.output_dir, self.output_file + ".pdf")
        add_links(no_links_output_file, output_file_final, self.links_register)

        if self.cleanup:
            for file in detailed_pages_files:
                if os.path.exists(file):
                    os.remove(file)
            if os.path.exists(overview_file_path):
                os.remove(overview_file_path)
            if os.path.exists(no_links_output_file):
                os.remove(no_links_output_file)

        return output_file_final

    def add_time_frame_column(self, fig: OverviewPage, time_frame: TimeFrame, number: int):
        column = Column(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            header_title=self.translator.get_label(time_frame.description),
            header_subtitle=helper.get_subtitle(time_frame),
            header_color=helper.get_header_color(time_frame),
            number=number,
        )

        fig.columns.append(column)

    def create_details_page(
        self,
        page_number: int,
        title: str,
        link_target: str,
        questions: list[ResearchQuestion],
    ) -> DetailsPage:
        dwg_details_page = DetailsPage(
            page_number=page_number,
            title=title,
            title_link_target=link_target,
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
        )
        for question in sorted(questions, key=lambda q: q.id):
            dwg_details_page.questions.append(
                QuestionDetails(
                    layout_configuration=self.layout_configuration,
                    links_register=self.links_register,
                    translator=self.translator,
                    research_question=question,
                )
            )

        return dwg_details_page
