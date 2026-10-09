"""
Copyright (C) Stichting Deltares 2026. All rights reserved.

This file is part of the 6svk toolbox.

This program is free software; you can redistribute it and/or modify it under the terms of
the GNU Lesser General Public License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with this
program; if not, see <https://www.gnu.org/licenses/>.

All names, logos, and references to "Deltares" are registered trademarks of Stichting
Deltares and remain full property of Stichting Deltares at all times. All rights reserved.
"""

from collections import defaultdict
from typing import DefaultDict

from svk.data import (
    StormSurgeBarrierResearchQuestion,
    StormSurgeBarrier,
    TimeFrame,
    ResearchLine,
    IconProvider,
    Translator,
    Label,
    StormSurgeBarrierResearchLineFactory,
    StormSurgeBarrierResearchLines,
    Grid,
    Color,  # TODO: Move base color away from research line
    KnownColors,
)
from svk.visualization.helpers._measuretext import measure_text
from svk.data.helpers import color_toward_grey
from svk.visualization.helpers import _calendar_helper as helper
from svk.visualization.helpers import _color_helper as colorhelper
from svk.visualization.elements._column import Column
from svk.visualization.elements._group import Group
from svk.visualization.elements._cluster import Cluster, ClusterColumn
from svk.visualization.elements._question_summary_element import QuestionSummaryElement
from svk.visualization.documents._document import ResearchQuestionsDocument
from svk.visualization.pages._page import Page
from svk.visualization.pages._time_line_overview_page import TimeLineOverviewPage
from svk.visualization.pages._lifetime_analysis_page import LifeTimeAnalysisPage


def _get_research_line_title(translator: Translator, research_line: ResearchLine | None) -> str:
    if research_line is None:
        return translator.get_label(Label.D_NoResearchLine)
    else:
        return str(research_line.number) + ". " + translator.get_label(research_line.title)


class ResearchAgendaDocument(ResearchQuestionsDocument):
    storm_surge_barrier: StormSurgeBarrier
    _clusters: dict[int, Cluster] = {}
    disclaimer: str | None = (
        "Dit is een eerste concept van de onderzoeksagenda stormvloedkeringen. Deze versie is ontstaan in samenwerking met de asset management teams van de keringen. De prioritering van de onderzoeksvragen moet nog gereviewd worden door o.a. de asset management teams en RWS WVL/GPO. De indeling in tijdsperiode is op dit moment in ontwikkeling. Voor vragen, neem contact op met Marit de Jong of Riva de Vries."
    )
    disclaimer_links: list[tuple[str, str]] | None = [
        ("Riva de Vries", "mailto:riva.de.vries@rws.nl"),
        ("Marit de Jong", "mailto:marit.de.jong@rws.nl"),
    ]
    etl_grid: Grid | None = None
    efl_grid: Grid | None = None

    def create_pages(self) -> list[Page]:
        self.layout_configuration.question_id_box_width = (
            max([measure_text(q.id, self.layout_configuration.font_size)[0] for q in self.questions])
            + 2 * self.layout_configuration.small_margin
        )
        pages = [
            self._create_overview_page(
                page_number=0,
                title=f"Onderzoeksagenda {self.translator.get_label(self.storm_surge_barrier.title)}",
                subtitle="Algemeen overzicht",
            ),
            self._create_overview_page(
                page_number=1,
                research_lines=[
                    StormSurgeBarrierResearchLineFactory.get_research_line_from_ssb_enum(
                        StormSurgeBarrierResearchLines.ConstructiveAspects
                    ),
                    StormSurgeBarrierResearchLineFactory.get_research_line_from_ssb_enum(StormSurgeBarrierResearchLines.OperatingSystem),
                    StormSurgeBarrierResearchLineFactory.get_research_line_from_ssb_enum(StormSurgeBarrierResearchLines.Facilities),
                    StormSurgeBarrierResearchLineFactory.get_research_line_from_ssb_enum(StormSurgeBarrierResearchLines.Maintenance),
                ],
                title=f"Overzicht onderzoeksagenda {self.translator.get_label(self.storm_surge_barrier.title)}",
                subtitle=self.translator.get_label(Label.RLG_Maintenance),
            ),
            self._create_overview_page(
                page_number=2,
                research_lines=[
                    StormSurgeBarrierResearchLineFactory.get_research_line_from_ssb_enum(StormSurgeBarrierResearchLines.Cyber),
                    StormSurgeBarrierResearchLineFactory.get_research_line_from_ssb_enum(StormSurgeBarrierResearchLines.Hydrodynamics),
                    StormSurgeBarrierResearchLineFactory.get_research_line_from_ssb_enum(
                        StormSurgeBarrierResearchLines.ProbabilityOfFailyre
                    ),
                    StormSurgeBarrierResearchLineFactory.get_research_line_from_ssb_enum(StormSurgeBarrierResearchLines.Adaptation),
                ],
                title=f"Overzicht onderzoeksagenda {self.translator.get_label(self.storm_surge_barrier.title)}",
                subtitle=self.translator.get_label(Label.RLG_Requirements),
            ),
            self._create_overview_page(
                page_number=3,
                research_lines=[
                    StormSurgeBarrierResearchLineFactory.get_research_line_from_ssb_enum(StormSurgeBarrierResearchLines.Organizational),
                    StormSurgeBarrierResearchLineFactory.get_research_line_from_ssb_enum(StormSurgeBarrierResearchLines.Lifespan),
                ],
                title=f"Overzicht onderzoeksagenda {self.translator.get_label(self.storm_surge_barrier.title)}",
                subtitle=self.translator.get_label(Label.RLG_Operational),
            ),
        ] + self.create_detailes_pages(current_page_number=4)

        if self.efl_grid is not None:
            pages.append(
                self._create_lifetime_analysis_page(
                    grid=self.efl_grid, subtitle="Einde Functionele Levensduur (EFL)", page_number=len(pages)
                )
            )

        if self.etl_grid is not None:
            pages.append(
                self._create_lifetime_analysis_page(
                    grid=self.etl_grid, subtitle="Einde Technische Levensduur (ETL)", page_number=len(pages)
                )
            )

        return pages

    def _create_overview_page(
        self,
        page_number: int,
        title: str,
        subtitle: str,
        research_lines: list[ResearchLine] | None = None,
    ) -> TimeLineOverviewPage:
        time_groups = defaultdict(list[StormSurgeBarrierResearchQuestion])

        questions = ([q for q in self.questions if q.research_line in research_lines]) if research_lines else list(self.questions)
        for q in questions:
            time_groups[q.time_frame].append(q)

        fig = TimeLineOverviewPage(
            page_number=page_number,
            title=title,
            subtitle=subtitle,
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            icon=IconProvider.create_icon(self.storm_surge_barrier),
            disclaimer=self.disclaimer,
            disclaimer_links=self.disclaimer_links,
            columns=tuple(
                [
                    self.get_time_frame_column(time_frame=TimeFrame.Now, number=0),
                    self.get_time_frame_column(time_frame=TimeFrame.NearFuture, number=1),
                    self.get_time_frame_column(time_frame=TimeFrame.Future, number=2),
                ]
            ),
            clusters=self.get_clusters(questions=questions, page_number=page_number),
        )

        return fig

    def get_time_frame_column(
        self,
        time_frame: TimeFrame,
        number: int,
    ) -> Column:
        return Column(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            header_title=self.translator.get_label(time_frame.description),
            header_subtitle=helper.get_subtitle(time_frame),
            header_color=colorhelper.get_color(layout_configuration=self.layout_configuration, time_frame=time_frame),
            number=number,
        )

    def get_clusters(self, questions: list[StormSurgeBarrierResearchQuestion], page_number: int) -> tuple[Cluster, ...]:
        time_frame_column_numbers: dict[TimeFrame, int] = {
            TimeFrame.Now: 0,
            TimeFrame.NearFuture: 1,
            TimeFrame.Future: 2,
        }

        questions_by_cluster: defaultdict[int, list[StormSurgeBarrierResearchQuestion]] = defaultdict(
            list[StormSurgeBarrierResearchQuestion]
        )
        for question in questions:
            if question.research_line is not None:
                questions_by_cluster[question.research_line.cluster].append(question)

        clusters: list[Cluster] = []
        for i_cluster in questions_by_cluster:
            questions_per_time_frame_column: defaultdict[int, list[StormSurgeBarrierResearchQuestion]] = defaultdict(
                list[StormSurgeBarrierResearchQuestion]
            )
            for question in questions_by_cluster[i_cluster]:
                if question.time_frame in time_frame_column_numbers:
                    questions_per_time_frame_column[time_frame_column_numbers[question.time_frame]].append(question)

            columns: list[ClusterColumn] = []
            for i_column in questions_per_time_frame_column:
                questions_per_group_in_column: defaultdict[ResearchLine, list[StormSurgeBarrierResearchQuestion]] = defaultdict(
                    list[StormSurgeBarrierResearchQuestion]
                )

                base_color: Color = KnownColors.White
                for question in questions_per_time_frame_column[i_column]:
                    if question.research_line is not None:
                        base_color = question.research_line.base_color
                        questions_per_group_in_column[question.research_line].append(question)

                column_groups: list[Group] = []
                for research_line in questions_per_group_in_column:
                    question_elements = tuple(
                        [
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
                    )
                    time_frame = questions_per_group_in_column[research_line][0].time_frame
                    column_groups.append(
                        Group(
                            layout_configuration=self.layout_configuration,
                            links_register=self.links_register,
                            translator=self.translator,
                            page_number=page_number,
                            link_target_id=research_line.id,
                            title=_get_research_line_title(self.translator, research_line),
                            color=color_toward_grey(research_line.base_color, time_frame.grey_fraction),
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
                    columns=tuple(columns),
                )
            )

        return tuple(clusters)

    def _create_lifetime_analysis_page(self, grid: Grid, subtitle: str, page_number: int) -> Page:
        return LifeTimeAnalysisPage(
            page_number=page_number,
            title=f"Levensduuranalyse - {self.translator.get_label(self.storm_surge_barrier.title)}",
            subtitle=subtitle,
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            icon=IconProvider.create_icon(self.storm_surge_barrier),
            disclaimer=self.disclaimer,
            disclaimer_links=self.disclaimer_links,
            grid=grid,
        )
