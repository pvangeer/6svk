from collections import defaultdict
from datetime import datetime
from svk.data import (
    TimeFrame,
    ResearchLine,
    IconProvider,
    SluicesResearchLineFactory,
    Translator,
    SluicesResearchQuestion,
    Label,
    SluicesResearchLines,
)
from svk.visualization._layout_configuration import LayoutConfiguration
from svk.visualization.pages._page import Page
from svk.visualization.helpers import _calendar_helper as helper
from svk.visualization.helpers import _color_helper as colorhelper
from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.pages._page import Page
from svk.visualization.pages._time_line_overview_page import TimeLineOverviewPage
from svk.visualization.pages._sluices_question_details_page import SluicesQuestionDetailsPage
from svk.visualization.elements._column import Column
from svk.visualization.elements._group import Group
from svk.visualization.elements._cluster import Cluster
from svk.visualization.elements._question_summary_element import QuestionSummaryElement
from svk.visualization.elements.panheel._sluices_question_details_element import SluicesQuestionDetailsElement
from svk.visualization.documents._document import Document


def _get_research_line_title(translator: Translator, research_line: ResearchLine | None) -> str:
    if research_line is None:
        return translator.get_label(Label.D_NoResearchLine)
    else:
        return str(research_line.number) + ". " + translator.get_label(research_line.title)


class SluicesDocument(Document):
    questions: list[SluicesResearchQuestion]
    layout_configuration: LayoutConfiguration = LayoutConfiguration(use_rijkswaterstaat_colors=True, use_gradients=False)
    disclaimer: str | None = (
        f"Deze agenda is ontstaan in samenwerking met het asset management teams van sluis Panheel. Het weerspiegelt de kennisvragen op het moment van opstellen ({datetime.now().strftime("%Y-%m-%d")}). Voor vragen, neem contact op met Meinard Tiessen."
    )
    disclaimer_links: list[tuple[str, str]] | None = [
        ("Meinard Tiessen", "mailto:meinard.tiessen@deltares.nl"),
    ]

    def create_pages(self) -> list[Page]:
        return [
            self._create_overview_page(
                page_number=0,
                research_lines=[
                    SluicesResearchLineFactory.get_research_line_from_ssb_enum(SluicesResearchLines.TechnicalLifeTimeCivilParts),
                    SluicesResearchLineFactory.get_research_line_from_ssb_enum(SluicesResearchLines.TechnicalLifeTimeInstallations),
                    SluicesResearchLineFactory.get_research_line_from_ssb_enum(SluicesResearchLines.InspectionsMonitoringAndData),
                ],
                subtitle=self.translator.get_label(Label.RLG_Maintenance),
            ),
            self._create_overview_page(
                page_number=1,
                research_lines=[
                    SluicesResearchLineFactory.get_research_line_from_ssb_enum(SluicesResearchLines.WaterSafety),
                    SluicesResearchLineFactory.get_research_line_from_ssb_enum(SluicesResearchLines.WaterSystemAndAvailability),
                    SluicesResearchLineFactory.get_research_line_from_ssb_enum(SluicesResearchLines.EcologyAndWaterQuality),
                    SluicesResearchLineFactory.get_research_line_from_ssb_enum(SluicesResearchLines.Functions),
                    SluicesResearchLineFactory.get_research_line_from_ssb_enum(SluicesResearchLines.Operation),
                    SluicesResearchLineFactory.get_research_line_from_ssb_enum(SluicesResearchLines.Robustness),
                    SluicesResearchLineFactory.get_research_line_from_ssb_enum(SluicesResearchLines.Strategy),
                    SluicesResearchLineFactory.get_research_line_from_ssb_enum(SluicesResearchLines.EnvironmentalImpact),
                ],
                subtitle=self.translator.get_label(Label.RLG_Requirements),
            ),
            self._create_overview_page(
                page_number=2,
                research_lines=[SluicesResearchLineFactory.get_research_line_from_ssb_enum(SluicesResearchLines.Organizational)],
                subtitle=self.translator.get_label(Label.RLG_Operational),
            ),
        ] + self.create_detailed_sluice_question_pages(current_page_number=3)

    def _create_overview_page(
        self,
        page_number: int,
        research_lines: list[ResearchLine],
        subtitle: str,
    ) -> TimeLineOverviewPage:
        self.layout_configuration.question_id_box_width = (
            max([measure_text(q.id, self.layout_configuration.font_size)[0] for q in self.questions])
            + 2 * self.layout_configuration.small_margin
        )

        fig = TimeLineOverviewPage(
            page_number=page_number,
            title="Overzicht kennisagenda Sluis Panheel",
            subtitle=subtitle,
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            icon=IconProvider.create_rws_sluice_icon(),
            disclaimer=self.disclaimer,
            disclaimer_links=self.disclaimer_links,
        )

        self.add_time_frame_column(fig=fig, time_frame=TimeFrame.Now, number=0, color_group=research_lines[0].cluster)
        self.add_time_frame_column(fig=fig, time_frame=TimeFrame.NearFuture, number=1, color_group=research_lines[0].cluster)
        self.add_time_frame_column(fig=fig, time_frame=TimeFrame.Future, number=2, color_group=research_lines[0].cluster)
        self.add_clusters_per_research_line(
            fig=fig, questions=[q for q in self.questions if q.research_line in research_lines], page_number=page_number
        )
        return fig

    def add_time_frame_column(self, fig: TimeLineOverviewPage, time_frame: TimeFrame, number: int, color_group: int):
        column = Column(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            header_title=self.translator.get_label(time_frame.description),
            header_subtitle=helper.get_subtitle(time_frame),
            header_color=colorhelper.get_color(self.layout_configuration, time_frame, research_line_group=color_group),
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
        grouped_questions_lists: defaultdict[tuple[TimeFrame, ResearchLine], list[SluicesResearchQuestion]] = defaultdict(
            list[SluicesResearchQuestion]
        )

        for question in questions:
            if question.research_line is None or question.time_frame not in time_frame_column_numbers:
                continue
            grouped_questions_lists[(question.time_frame, question.research_line)].append(question)

        for questions_list_key in sorted(grouped_questions_lists, key=lambda kv: (kv[1].number, time_frame_column_numbers[kv[0]])):
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
                page_number=page_number,
                link_target_id=current_research_line.id,
                title=_get_research_line_title(self.translator, current_research_line),
                color=colorhelper.get_color(
                    self.layout_configuration, current_time_frame, research_line_group=current_research_line.cluster
                ),
                use_contrast_color=True,
            )

            cluster.groups[time_frame_column_numbers[current_time_frame]].append(new_group)
            for question in sorted(grouped_questions_lists[questions_list_key], key=lambda q: q.priority, reverse=True):
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
                    title="Details kennisagenda Sluis Panheel",
                    subtitle=_get_research_line_title(self.translator, research_line),
                    link_target=research_line.id,
                    questions=grouped_questions[research_line],
                )
            )
            current_page_number += 1

        if len(non_grouped) > 0:
            pages.append(
                self.create_details_page(
                    page_number=current_page_number,
                    title="Details kennisagenda Sluis Panheel",
                    subtitle=_get_research_line_title(self.translator, None),
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
        subtitle: str | None = None,
    ) -> Page:
        dwg_details_page = SluicesQuestionDetailsPage(
            page_number=page_number,
            title=title,
            subtitle=subtitle,
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
