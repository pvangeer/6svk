from pydantic import BaseModel
from collections import defaultdict
from typing import DefaultDict
import os

from svk.data import ResearchQuestion, StormSurgeBarrier, TimeFrame, LinksRegister, ResearchLine, Translator
from svk.io import svg_to_pdf_chrome, merge_pdf_files, add_links


from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.helpers._greyfraction import color_toward_grey
from svk.visualization.helpers import _calendar_helper as helper
from svk.visualization._layout_configuration import LayoutConfiguration
from svk.visualization._overview_page import OverviewPage
from svk.visualization._details_page import DetailsPage
from svk.visualization._question_details import QuestionDetails
from svk.visualization._column import Column
from svk.visualization._group import Group
from svk.visualization._cluster import Cluster
from svk.visualization._question import Question


class KnowledgeCalendar(BaseModel):
    layout_configuration: LayoutConfiguration = LayoutConfiguration()
    links_register: LinksRegister = LinksRegister()
    translator: Translator = Translator(lang="nl")
    storm_surge_barrier: StormSurgeBarrier
    questions: list[ResearchQuestion]
    output_dir: str
    output_file: str
    _clusters: dict[int, Cluster] = {}

    def build(self):
        # build overview page
        overview = self.create_overview_page_from_questions(
            page_number=0, title=self.translator.get_label(self.storm_surge_barrier.title), questions=self.questions
        )

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
                title=str(research_line.number) + ". " + self.translator.get_label(research_line.title),
                questions=grouped_questions[research_line],
            )
            page_number += 1

        if len(non_grouped) > 0:
            uncategorized_page = self.create_details_page_from_questions(
                page_number=page_number,
                title="Zonder onderzoekslijn",
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
            max([measure_text(q.id, self.layout_configuration.font_size)[0] for q in questions]) + self.layout_configuration.small_margin
        )

        fig = OverviewPage(
            page_number=page_number,
            title=title,
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            storm_surge_barrier=self.storm_surge_barrier,
        )
        self.add_column(fig=fig, questions=time_groups[TimeFrame.Now], time_frame=TimeFrame.Now, number=0)
        self.add_column(fig=fig, questions=time_groups[TimeFrame.NearFuture], time_frame=TimeFrame.NearFuture, number=1)
        self.add_column(fig=fig, questions=time_groups[TimeFrame.Future], time_frame=TimeFrame.Future, number=2)
        fig.clusters = list(self._clusters.values())
        return fig

    def create_details_page_from_questions(
        self,
        page_number: int,
        title: str,
        questions: list[ResearchQuestion],
    ) -> DetailsPage:
        dwg_details_page = DetailsPage(
            page_number=page_number,
            title=title,
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

    def add_column(self, fig: OverviewPage, questions: list[ResearchQuestion], time_frame: TimeFrame, number: int):
        column = Column(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            header_title=self.translator.get_label(time_frame.description),
            header_subtitle=helper.get_subtitle(time_frame),
            header_color=helper.get_header_color(time_frame),
            number=number,
        )

        if len(questions) > 0:
            now_questions_groups: DefaultDict[ResearchLine, list[ResearchQuestion]] = defaultdict(list)
            for q in questions:
                if q.research_line_primary is None:
                    # TODO: This should not occur here.
                    continue
                now_questions_groups[q.research_line_primary].append(q)

            for research_line in sorted(now_questions_groups.keys(), key=lambda g: g.number):
                if research_line.cluster not in self._clusters:
                    cluster = Cluster(
                        layout_configuration=self.layout_configuration,
                        links_register=self.links_register,
                        translator=self.translator,
                        color=research_line.base_color,
                    )
                    self._clusters[research_line.cluster] = cluster
                else:
                    cluster = self._clusters[research_line.cluster]

                new_group = Group(
                    layout_configuration=self.layout_configuration,
                    links_register=self.links_register,
                    translator=self.translator,
                    title=self.translator.get_label(research_line.title),
                    color=color_toward_grey(research_line.base_color, time_frame.grey_fraction),
                )
                cluster.groups[column.number].append(new_group)
                for question in sorted(now_questions_groups[research_line], key=helper.get_priority, reverse=True):
                    new_group.questions.append(
                        Question(
                            layout_configuration=self.layout_configuration,
                            links_register=self.links_register,
                            translator=self.translator,
                            research_question=question,
                        )
                    )

            fig.columns.append(column)
