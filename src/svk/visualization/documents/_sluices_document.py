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
    Color,  # TODO: Move base_color from research_line to some factory and do not pass colors around related to research lines.
    KnownColors,
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
from svk.visualization.elements._cluster import Cluster, ClusterColumn
from svk.visualization.elements._question_summary_element import QuestionSummaryElement
from svk.visualization.elements.panheel._sluices_question_details_element import SluicesQuestionDetailsElement
from svk.visualization.documents._document import Document
from svk.visualization.pages._legend_page import LegendPage


def _get_research_line_title(translator: Translator, research_line: ResearchLine | None) -> str:
    if research_line is None:
        return translator.get_label(Label.D_NoResearchLine)
    else:
        return str(research_line.number) + ". " + translator.get_label(research_line.title)


class SluicesDocument(Document):
    questions: list[SluicesResearchQuestion]
    layout_configuration: LayoutConfiguration = LayoutConfiguration(use_rijkswaterstaat_colors=True, use_gradients=False)
    disclaimer: str | None = (
        f"Deze agenda is opgesteld op {datetime.now().strftime("%Y-%m-%d")} in samenwerking met het asset management team van sluis Panheel. Voor vragen, neem contact op met Meinard Tiessen."
    )
    disclaimer_links: list[tuple[str, str]] | None = [
        ("Meinard Tiessen", "mailto:meinard.tiessen@deltares.nl"),
    ]

    def create_pages(self) -> list[Page]:
        pages = [
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
        ] + self._create_detailed_sluice_question_pages(current_page_number=3)
        pages += [self._create_legend_page(page_number=len(pages))]

        return pages

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
            include_legend_link=True,
            columns=tuple(
                [
                    self.get_time_frame_column(time_frame=TimeFrame.Now, number=0, color_group=research_lines[0].cluster),
                    self.get_time_frame_column(time_frame=TimeFrame.NearFuture, number=1, color_group=research_lines[0].cluster),
                    self.get_time_frame_column(time_frame=TimeFrame.Future, number=2, color_group=research_lines[0].cluster),
                ]
            ),
            clusters=list(
                self.get_clusters(questions=[q for q in self.questions if q.research_line in research_lines], page_number=page_number)
            ),
        )

        return fig

    def get_time_frame_column(self, time_frame: TimeFrame, number: int, color_group: int) -> Column:
        return Column(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            header_title=self.translator.get_label(time_frame.description),
            header_subtitle=helper.get_subtitle(time_frame),
            header_color=colorhelper.get_color(self.layout_configuration, time_frame, research_line_group=color_group),
            number=number,
        )

    def get_clusters(self, questions: list[SluicesResearchQuestion], page_number: int) -> tuple[Cluster, ...]:
        time_frame_column_numbers: dict[TimeFrame, int] = {
            TimeFrame.Now: 0,
            TimeFrame.NearFuture: 1,
            TimeFrame.Future: 2,
        }

        questions_by_cluster: defaultdict[int, list[SluicesResearchQuestion]] = defaultdict(list[SluicesResearchQuestion])
        for question in questions:
            if question.research_line is not None:
                questions_by_cluster[question.research_line.cluster].append(question)

        clusters: list[Cluster] = []
        for i_cluster in questions_by_cluster:
            questions_per_time_frame_column: defaultdict[int, list[SluicesResearchQuestion]] = defaultdict(list[SluicesResearchQuestion])
            for question in questions_by_cluster[i_cluster]:
                if question.time_frame in time_frame_column_numbers:
                    questions_per_time_frame_column[time_frame_column_numbers[question.time_frame]].append(question)

            columns: list[ClusterColumn] = []
            for i_column in questions_per_time_frame_column:
                questions_per_group_in_column: defaultdict[ResearchLine, list[SluicesResearchQuestion]] = defaultdict(
                    list[SluicesResearchQuestion]
                )

                base_color: Color = KnownColors.White
                for question in questions_per_time_frame_column[i_column]:
                    if question.research_line is not None:
                        base_color = question.research_line.base_color
                        questions_per_group_in_column[question.research_line].append(question)

                column_groups: list[Group] = []
                for research_line in questions_per_group_in_column:
                    question_elements = [
                        QuestionSummaryElement(
                            layout_configuration=self.layout_configuration,
                            links_register=self.links_register,
                            translator=self.translator,
                            research_question=q,
                            page_number=page_number,
                            show_priority=True,
                        )
                        for q in questions_per_group_in_column[research_line]
                    ]
                    time_frame = questions_per_group_in_column[research_line][0].time_frame
                    column_groups.append(
                        Group(
                            layout_configuration=self.layout_configuration,
                            links_register=self.links_register,
                            translator=self.translator,
                            page_number=page_number,
                            link_target_id=research_line.id,
                            title=_get_research_line_title(self.translator, research_line),
                            color=colorhelper.get_color(self.layout_configuration, time_frame, research_line_group=research_line.cluster),
                            use_contrast_color=True,
                            questions=question_elements,
                        )
                    )

                columns.append(ClusterColumn(column_number=i_column, groups=tuple(column_groups)))

            clusters.append(
                Cluster(
                    layout_configuration=self.layout_configuration,
                    links_register=self.links_register,
                    translator=self.translator,
                    color=base_color,
                    group_column=tuple(columns),
                )
            )

        return tuple(clusters)

    def _create_detailed_sluice_question_pages(self, current_page_number: int) -> list[Page]:
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
            include_legend_link=True,
            questions=tuple(
                SluicesQuestionDetailsElement(
                    layout_configuration=self.layout_configuration,
                    links_register=self.links_register,
                    translator=self.translator,
                    research_question=question,
                    page_number=page_number,
                )
                for question in questions
            ),
        )
        return dwg_details_page

    def _create_legend_page(self, page_number: int) -> Page:
        page = LegendPage(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            title="Verklaring",
            subtitle="Gebruikte symbolen en kleuren en vraagcodes",
            page_number=page_number,
            disclaimer=self.disclaimer,
            disclaimer_links=self.disclaimer_links,
        )
        return page
