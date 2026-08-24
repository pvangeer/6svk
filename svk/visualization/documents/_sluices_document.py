from collections import defaultdict
from svk.data import TimeFrame, ResearchLine, StormSurgeBarrier
from svk.visualization.pages._page import Page
from svk.visualization.helpers import _calendar_helper as helper
from svk.visualization.helpers._measuretext import measure_text
from svk.data.helpers._greyfraction import color_toward_grey
from svk.visualization.pages._time_line_overview_page import TimeLineOverviewPage
from svk.visualization.elements._column import Column
from svk.visualization.elements._group import Group
from svk.visualization.elements._cluster import Cluster
from svk.visualization.elements._question_summary_element import QuestionSummaryElement
from svk.visualization.elements.panheel._sluices_question_details_element import SluicesQuestionDetailsElement

from svk.data import SluicesResearchQuestion, TimeFrame, Label
from svk.visualization.documents._document import Document
from svk.visualization.pages._page import Page
from svk.visualization.pages._time_line_overview_page import TimeLineOverviewPage
from svk.visualization.pages._sluices_question_details_page import SluicesQuestionDetailsPage
from svk.visualization.helpers._measuretext import measure_text


class SluicesDocument(Document):
    questions: list[SluicesResearchQuestion]

    def create_pages(self) -> list[Page]:
        return [self._create_overview_page(page_number=0)] + self.create_detailed_sluice_question_pages(current_page_number=1)

    # TODO: CReate shared methods over all overview pages.
    def _create_overview_page(
        self,
        page_number: int,
    ) -> TimeLineOverviewPage:
        self.layout_configuration.question_id_box_width = (
            max([measure_text(q.id, self.layout_configuration.font_size)[0] for q in self.questions])
            + 2 * self.layout_configuration.small_margin
        )

        fig = TimeLineOverviewPage(
            page_number=page_number,
            title="Kennisvragen Sluis Panheel",
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            icon=StormSurgeBarrier.SluicePanheel,
            disclaimer=self.disclaimer,
            disclaimer_links=self.disclaimer_links,
        )

        self.add_time_frame_column(fig=fig, time_frame=TimeFrame.Now, number=0)
        self.add_time_frame_column(fig=fig, time_frame=TimeFrame.NearFuture, number=1)
        self.add_time_frame_column(fig=fig, time_frame=TimeFrame.Future, number=2)
        self.add_clusters_per_research_line(fig=fig, questions=self.questions, page_number=page_number)
        return fig

    def add_time_frame_column(self, fig: TimeLineOverviewPage, time_frame: TimeFrame, number: int):
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

    def add_clusters_per_research_line(self, fig: TimeLineOverviewPage, questions: list[SluicesResearchQuestion], page_number: int):
        clusters: dict[int, Cluster] = {}
        time_frame_column_numbers: dict[TimeFrame, int] = {
            TimeFrame.Now: 0,
            TimeFrame.NearFuture: 1,
            TimeFrame.Future: 2,
        }
        grouped_quenstions_lists: defaultdict[tuple[TimeFrame, ResearchLine], list[SluicesResearchQuestion]] = defaultdict(
            list[SluicesResearchQuestion]
        )

        for question in questions:
            if question.research_line is None or question.time_frame not in time_frame_column_numbers:
                continue
            grouped_quenstions_lists[(question.time_frame, question.research_line)].append(question)

        for questions_list_key in sorted(grouped_quenstions_lists, key=lambda kv: (kv[1].number, time_frame_column_numbers[kv[0]])):
            current_time_frame = questions_list_key[0]
            current_research_line = questions_list_key[1]

            if current_research_line.cluster not in clusters:
                clusters[current_research_line.cluster] = Cluster(
                    layout_configuration=self.layout_configuration,
                    links_register=self.links_register,
                    translator=self.translator,
                    color=current_research_line.base_color,
                )

            cluster = clusters[current_research_line.cluster]

            new_group = Group(
                layout_configuration=self.layout_configuration,
                links_register=self.links_register,
                translator=self.translator,
                title=self.translator.get_label(current_research_line.title),
                color=color_toward_grey(current_research_line.base_color, current_time_frame.grey_fraction),
            )

            cluster.groups[time_frame_column_numbers[current_time_frame]].append(new_group)
            for question in sorted(grouped_quenstions_lists[questions_list_key], key=lambda q: q.priority, reverse=True):
                new_group.questions.append(
                    QuestionSummaryElement(
                        layout_configuration=self.layout_configuration,
                        links_register=self.links_register,
                        translator=self.translator,
                        research_question=question,
                        page_number=page_number,
                        show_priority=True,
                    )
                )

        fig.clusters = list(clusters.values())

    def create_detailed_sluice_question_pages(self, current_page_number: int) -> list[Page]:
        pages: list[Page] = []

        grouped_questions: defaultdict[ResearchLine, list[SluicesResearchQuestion]] = defaultdict(list[SluicesResearchQuestion])
        non_grouped: list[SluicesResearchQuestion] = []
        for question in self.questions:
            if question.research_line is None:
                non_grouped.append(question)
            else:
                grouped_questions[question.research_line].append(question)

        for research_line in sorted(grouped_questions, key=lambda r_l: r_l.number):
            pages.append(
                self.create_details_page(
                    page_number=current_page_number,
                    title=str(research_line.number) + ". " + self.translator.get_label(research_line.title),
                    link_target=research_line.id,
                    questions=grouped_questions[research_line],
                )
            )
            current_page_number += 1

        if len(non_grouped) > 0:
            pages.append(
                self.create_details_page(
                    page_number=current_page_number,
                    title=self.translator.get_label(Label.D_NoResearchLine),
                    link_target="",
                    questions=non_grouped,
                )
            )

        return pages

    def create_details_page(
        self,
        page_number: int,
        title: str,
        link_target: str,
        questions: list[SluicesResearchQuestion],
    ) -> Page:
        dwg_details_page = SluicesQuestionDetailsPage(
            page_number=page_number,
            title=title,
            title_link_target=link_target,
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            disclaimer=self.disclaimer,
            disclaimer_links=self.disclaimer_links,
        )
        for question in sorted(questions, key=lambda q: q.id):
            dwg_details_page.questions.append(
                SluicesQuestionDetailsElement(
                    layout_configuration=self.layout_configuration,
                    links_register=self.links_register,
                    translator=self.translator,
                    research_question=question,
                    page_number=page_number,
                )
            )

        return dwg_details_page
