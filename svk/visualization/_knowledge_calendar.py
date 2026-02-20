from pydantic import BaseModel
from collections import defaultdict
from typing import DefaultDict
import os

from svk.data import ResearchQuestion, StormSurgeBarrier, TimeFrame, LinksRegister, ResearchLine
from svk.io import svg_to_pdf_chrome, merge_pdf_files, add_links

from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.helpers._greyfraction import color_toward_grey

from svk.visualization._layout_configuration import LayoutConfiguration
from svk.visualization._overview_page import OverviewPage
from svk.visualization._details_page import DetailsPage
from svk.visualization._question_details import QuestionDetails
from svk.visualization._column import Column
from svk.visualization._group import Group
from svk.visualization._question import Question


class KnowledgeCalendar(BaseModel):
    layout_configuration: LayoutConfiguration = LayoutConfiguration()
    links_register: LinksRegister = LinksRegister()
    storm_surge_barrier: StormSurgeBarrier
    questions: list[ResearchQuestion]
    output_dir: str
    output_file: str

    def build(self):
        # build overview page
        overview = self.create_overview_page_from_questions(page_number=0, title=self.storm_surge_barrier.title, questions=self.questions)

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
            details_pages[research_line] = self.create_details_page_from_questions(
                page_number=page_number,
                title=str(research_line.number) + ". " + research_line.title,
                questions=grouped_questions[research_line],
            )
            page_number += 1

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
            svg_to_pdf_chrome(svg_dwg=details_pages[r_l].draw(), pdf_path=uncategorized_file_name)

        no_links_output_file = os.path.join(self.output_dir, self.output_file + " - no links.pdf")
        merge_pdf_files([overview_file_path] + detailed_pages_files, no_links_output_file)

        # implement links
        output_file_final = os.path.join(self.output_dir, self.output_file + ".pdf")
        add_links(no_links_output_file, output_file_final, self.links_register)
        return output_file_final

    def create_overview_page_from_questions(
        self,
        page_number: int,
        title: str,
        questions: list[ResearchQuestion],
    ) -> OverviewPage:
        time_groups = defaultdict(list[ResearchQuestion])

        for q in questions:
            time_groups[q.time_frame].append(q)

        self.layout_configuration.question_id_box_width = (
            max([measure_text(q.id, self.layout_configuration.font_size)[0] for q in questions]) + self.layout_configuration.line_margin
        )

        fig = OverviewPage(
            page_number=page_number,
            title=title,
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            storm_surge_barrier=self.storm_surge_barrier,
        )
        self.add_column(fig=fig, time_groups=time_groups, time_frame=TimeFrame.Now)
        self.add_column(fig=fig, time_groups=time_groups, time_frame=TimeFrame.NearFuture)
        self.add_column(fig=fig, time_groups=time_groups, time_frame=TimeFrame.Future)
        return fig

    def create_details_page_from_questions(
        self,
        page_number: int,
        title: str,
        questions: list[ResearchQuestion],
    ) -> DetailsPage:
        # TODO: Pass page title and implement. Use this to split large lists of questions and group them by research line in a separate page.
        dwg_details_page = DetailsPage(
            page_number=page_number, title=title, layout_configuration=self.layout_configuration, links_register=self.links_register
        )
        for question in sorted(questions, key=lambda q: q.id):
            dwg_details_page.questions.append(
                QuestionDetails(
                    layout_configuration=self.layout_configuration, links_register=self.links_register, research_question=question
                )
            )

        return dwg_details_page

    @staticmethod
    def get_priority(question: ResearchQuestion) -> int:
        return 1 if question.has_priority else 0

    @staticmethod
    def get_column_title(time_frame: TimeFrame) -> str:
        match time_frame:
            case TimeFrame.Now:
                return "Nu"
            case TimeFrame.NearFuture:
                return "Nabije toekomst"
            case TimeFrame.Future:
                return "Toekomst"
            case TimeFrame.NotRelevant:
                return "Niet relevant"
            case TimeFrame.Unknown:
                return "Onbekend"
            case _:
                raise ValueError("Unknown time frame")

    @staticmethod
    def get_subtitle(time_frame: TimeFrame) -> str:
        match time_frame:
            case TimeFrame.Now:
                return ""
            case TimeFrame.NearFuture:
                return "(2033 - 2040)"
            case TimeFrame.Future:
                return "(>2040)"
            case TimeFrame.NotRelevant:
                return "(-)"
            case TimeFrame.Unknown:
                return "(?)"
            case _:
                raise ValueError("Unknown time frame")

    @staticmethod
    def get_header_color(time_frame: TimeFrame) -> str:
        return color_toward_grey((18, 103, 221), grey_fraction=time_frame.grey_fraction)

    def add_column(self, fig: OverviewPage, time_groups, time_frame: TimeFrame):
        column = Column(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            header_title=KnowledgeCalendar.get_column_title(time_frame),
            header_subtitle=KnowledgeCalendar.get_subtitle(time_frame),
            header_color=KnowledgeCalendar.get_header_color(time_frame),
        )

        filtered_questions = time_groups[time_frame]
        if len(filtered_questions) > 0:
            now_questions_groups: DefaultDict[ResearchLine, list[ResearchQuestion]] = defaultdict(list)
            for q in filtered_questions:
                now_questions_groups[q.research_line_primary].append(q)

            for group in sorted(now_questions_groups.keys(), key=lambda g: g.number):
                fig.layout_configuration.cluster_colors[group.cluster] = group.base_color
                column.groups[group.cluster] = Group(
                    layout_configuration=self.layout_configuration,
                    links_register=self.links_register,
                    title=group.title,
                    color=color_toward_grey(group.base_color, time_frame.grey_fraction),
                )
                for question in sorted(now_questions_groups[group], key=KnowledgeCalendar.get_priority, reverse=True):
                    column.groups[group.cluster].questions.append(
                        Question(
                            layout_configuration=self.layout_configuration, links_register=self.links_register, research_question=question
                        )
                    )

            fig.columns.append(column)
