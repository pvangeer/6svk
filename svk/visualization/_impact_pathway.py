from pydantic import BaseModel
from collections import defaultdict
from typing import DefaultDict
import os

from svk.data import ImpactPathwayResearchQuestion, StormSurgeBarrier, TimeFrame, LinksRegister, ResearchLine, ImpactCategory, Translator
from svk.io import svg_to_pdf_chrome, merge_pdf_files, add_links

from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.helpers._greyfraction import color_toward_grey
from svk.visualization.helpers import _calendar_helper as helper
from svk.visualization._layout_configuration import LayoutConfiguration
from svk.visualization._overview_page import OverviewPage
from svk.visualization._details_page import DetailsPage
from svk.visualization._question_details import QuestionDetails
from svk.visualization._column import Column
from svk.visualization._group import Group, PlainTextGroup
from svk.visualization._cluster import Cluster
from svk.visualization._question import Question


# TODO: Merge logic with KnowledgeCalendar if possible
class ImpactPathway(BaseModel):
    layout_configuration: LayoutConfiguration = LayoutConfiguration()
    links_register: LinksRegister = LinksRegister()
    questions: list[ImpactPathwayResearchQuestion]
    translator: Translator = Translator(lang="en")
    output_dir: str
    output_file: str

    def build(self):
        # build overview page
        overview = self.create_overview_page_from_questions(page_number=0, questions=self.questions)

        # build detailed pages
        grouped_questions: defaultdict[ResearchLine, list[ImpactPathwayResearchQuestion]] = defaultdict(list[ImpactPathwayResearchQuestion])
        non_grouped: list[ImpactPathwayResearchQuestion] = []
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
                title_link_target=research_line.id,
                questions=grouped_questions[research_line],
            )
            page_number += 1

        if len(non_grouped) > 0:
            uncategorized_page = self.create_details_page_from_questions(
                page_number=page_number,
                title="No research line",
                title_link_target="",
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
        questions: list[ImpactPathwayResearchQuestion],
    ) -> OverviewPage:
        self.layout_configuration.question_id_box_width = (
            max([measure_text(q.id, self.layout_configuration.font_size)[0] for q in questions]) + self.layout_configuration.small_margin
        )

        fig = OverviewPage(
            page_number=page_number,
            title="Impact pathway",
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            storm_surge_barrier=StormSurgeBarrier.All,
        )
        self.add_column(fig=fig, time_frame=TimeFrame.Now, number=0)
        self.add_column(fig=fig, time_frame=TimeFrame.NearFuture, number=1)
        self.add_column(fig=fig, time_frame=TimeFrame.Future, number=2)
        # The impact column
        fig.columns.append(
            Column(
                layout_configuration=self.layout_configuration,
                links_register=self.links_register,
                translator=self.translator,
                header_title="",
                header_subtitle="",
                header_color="",
                number=3,
            )
        )
        self.add_clusters(fig=fig, questions=questions)

        return fig

    def create_details_page_from_questions(
        self,
        page_number: int,
        title: str,
        title_link_target: str,
        questions: list[ImpactPathwayResearchQuestion],
    ) -> DetailsPage:
        dwg_details_page = DetailsPage(
            page_number=page_number,
            title=title,
            title_link_target=title_link_target,
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

    def add_column(self, fig: OverviewPage, time_frame: TimeFrame, number: int):
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

    def add_clusters(self, fig: OverviewPage, questions: list[ImpactPathwayResearchQuestion]):
        clusters: dict[int, Cluster] = {}
        time_frame_column_numbers: dict[TimeFrame, int] = {
            TimeFrame.Now: 0,
            TimeFrame.NearFuture: 1,
            TimeFrame.Future: 2,
        }

        grouped_quenstions_lists: defaultdict[tuple[TimeFrame, ImpactCategory, ResearchLine], list[ImpactPathwayResearchQuestion]] = (
            defaultdict(list[ImpactPathwayResearchQuestion])
        )

        for question in questions:
            if question.research_line_primary is None or question.time_frame not in time_frame_column_numbers:
                continue
            grouped_quenstions_lists[(question.time_frame, question.impact_category, question.research_line_primary)].append(question)

        for questions_list_key in sorted(
            grouped_quenstions_lists, key=lambda k: (k[1].number, k[2].number, time_frame_column_numbers[k[0]])
        ):
            current_time_frame = questions_list_key[0]
            current_impact_category = questions_list_key[1]
            current_research_line = questions_list_key[2]

            if current_impact_category.number not in clusters:
                clusters[current_impact_category.number] = Cluster(
                    layout_configuration=self.layout_configuration,
                    links_register=self.links_register,
                    translator=self.translator,
                    color=(180, 180, 180),
                )

            cluster = clusters[current_impact_category.number]

            new_group = Group(
                layout_configuration=self.layout_configuration,
                links_register=self.links_register,
                translator=self.translator,
                title=self.translator.get_label(current_research_line.title),
                color=color_toward_grey(current_research_line.base_color, current_time_frame.grey_fraction),
            )

            cluster.groups[time_frame_column_numbers[current_time_frame]].append(new_group)
            for question in sorted(grouped_quenstions_lists[questions_list_key], key=helper.get_priority, reverse=True):
                new_group.questions.append(
                    Question(
                        layout_configuration=self.layout_configuration,
                        links_register=self.links_register,
                        translator=self.translator,
                        research_question=question,
                    )
                )

        for category in [
            ImpactCategory.SocioEconomicAndEnvironment,
            ImpactCategory.ReliableSSB,
            ImpactCategory.MaintenanceDecisions,
            ImpactCategory.HumanCapical,
            ImpactCategory.Example,
        ]:
            clusters[category.number].groups[3].append(
                PlainTextGroup(
                    layout_configuration=self.layout_configuration,
                    links_register=self.links_register,
                    translator=self.translator,
                    text=category.description,
                )
            )
        fig.clusters = list(clusters.values())
