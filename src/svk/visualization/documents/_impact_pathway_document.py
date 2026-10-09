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
from typing import cast
from svk.data import ImpactPathwayResearchQuestion, TimeFrame, ResearchLine, ImpactCategory, Translator, IconProvider, Color, KnownColors
from svk.data.helpers import color_toward_grey
from svk.visualization.pages._page import Page
from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.pages._time_line_overview_page import TimeLineOverviewPage
from svk.visualization.elements._column import Column
from svk.visualization.elements._group import Group, PlainTextGroup
from svk.visualization.elements._cluster import Cluster, ClusterColumn
from svk.visualization.elements._question_summary_element import QuestionSummaryElement
from svk.visualization.documents._document import ResearchQuestionsDocument
from datetime import date


class ImpactPathwayDocument(ResearchQuestionsDocument):
    disclaimer: str | None = (
        f"This is the impact pathway of the NWO SSB-∆ project (version 0.9 - {date.today()}). For questions, please contact Esther van Baaren or Bram van Prooijen."
    )
    disclaimer_links: list[tuple[str, str]] | None = [
        ("Esther van Baaren", "mailto:esther.vanbaaren@deltares.nl"),
        ("Bram van Prooijen", "mailto:b.c.vanprooijen@tudelft.nl"),
    ]
    translator: Translator = Translator(lang="en")

    def create_pages(self) -> list[Page]:
        return [self._create_overview_page(page_number=0), self._create_impact_overview_page(page_number=1)] + self.create_detailes_pages(
            current_page_number=2
        )

    def _create_impact_overview_page(
        self,
        page_number: int,
    ) -> TimeLineOverviewPage:
        self.layout_configuration.question_id_box_width = (
            max([measure_text(q.id, self.layout_configuration.font_size)[0] for q in self.questions])
            + 2 * self.layout_configuration.small_margin
        )

        fig = TimeLineOverviewPage(
            page_number=page_number,
            title="SSB-∆ Impact Pathway",
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            icon=IconProvider.create_6svk_icon(),
            disclaimer=self.disclaimer,
            disclaimer_links=self.disclaimer_links,
            columns=tuple(
                [
                    self.get_time_frame_column(time_frame=TimeFrame.NearFuture, number=0),
                    self.get_time_frame_column(time_frame=TimeFrame.Future, number=1),
                    Column(
                        layout_configuration=self.layout_configuration,
                        links_register=self.links_register,
                        translator=self.translator,
                        header_title="",
                        header_subtitle="",
                        header_color=KnownColors.Blue,
                        number=2,
                    ),
                ]
            ),
            clusters=self.get_clusters_per_impact_category(
                questions=cast(list[ImpactPathwayResearchQuestion], self.questions), page_number=page_number
            ),
        )
        return fig

    def get_clusters_per_impact_category(self, questions: list[ImpactPathwayResearchQuestion], page_number: int) -> tuple[Cluster, ...]:
        time_frame_column_numbers: dict[TimeFrame, int] = {
            TimeFrame.NearFuture: 0,
            TimeFrame.Future: 1,
        }

        questions_by_impact_category: defaultdict[ImpactCategory, list[ImpactPathwayResearchQuestion]] = defaultdict(
            list[ImpactPathwayResearchQuestion]
        )
        for question in questions:
            if question.research_line is not None:
                questions_by_impact_category[question.impact_category].append(question)

        clusters: list[Cluster] = []
        for impact_category in questions_by_impact_category:
            questions_per_time_frame_column: defaultdict[int, list[ImpactPathwayResearchQuestion]] = defaultdict(
                list[ImpactPathwayResearchQuestion]
            )
            for question in questions_by_impact_category[impact_category]:
                questions_per_time_frame_column[time_frame_column_numbers[question.time_frame]].append(question)

            columns: list[ClusterColumn] = []
            for i_column in questions_per_time_frame_column:
                questions_per_group_in_column: defaultdict[ResearchLine, list[ImpactPathwayResearchQuestion]] = defaultdict(
                    list[ImpactPathwayResearchQuestion]
                )

                for question in questions_per_time_frame_column[i_column]:
                    if question.research_line is not None:
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
                            title=self.translator.get_label(research_line.title),
                            color=color_toward_grey(research_line.base_color, time_frame.grey_fraction),
                            use_contrast_color=True,
                            questions=question_elements,
                        )
                    )

                columns.append(ClusterColumn(column_number=i_column, groups=tuple(column_groups)))
            columns.append(
                ClusterColumn(
                    column_number=2,
                    groups=tuple(
                        [
                            PlainTextGroup(
                                layout_configuration=self.layout_configuration,
                                links_register=self.links_register,
                                translator=self.translator,
                                text=impact_category.description,
                            )
                        ]
                    ),
                )
            )
            clusters.append(
                Cluster(
                    layout_configuration=self.layout_configuration,
                    links_register=self.links_register,
                    translator=self.translator,
                    color=Color(r=180, g=180, b=180),
                    columns=tuple(columns),
                )
            )

        return tuple(clusters)

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
            title="Research agenda SSB-∆",
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            icon=IconProvider.create_6svk_icon(),
            disclaimer=self.disclaimer,
            disclaimer_links=self.disclaimer_links,
            columns=tuple(
                [
                    self.get_time_frame_column(time_frame=TimeFrame.NearFuture, number=0),
                    self.get_time_frame_column(time_frame=TimeFrame.Future, number=1),
                ]
            ),
            clusters=self.get_clusters(questions=cast(list[ImpactPathwayResearchQuestion], self.questions), page_number=page_number),
        )

        self.get_clusters(questions=cast(list[ImpactPathwayResearchQuestion], self.questions), page_number=page_number)
        return fig

    def get_clusters(self, questions: list[ImpactPathwayResearchQuestion], page_number: int) -> tuple[Cluster, ...]:
        time_frame_column_numbers: dict[TimeFrame, int] = {
            TimeFrame.NearFuture: 0,
            TimeFrame.Future: 1,
        }

        questions_by_cluster: defaultdict[int, list[ImpactPathwayResearchQuestion]] = defaultdict(list[ImpactPathwayResearchQuestion])
        for question in questions:
            if question.research_line is not None:
                questions_by_cluster[question.research_line.cluster].append(question)

        clusters: list[Cluster] = []
        for i_cluster in questions_by_cluster:
            questions_per_time_frame_column: defaultdict[int, list[ImpactPathwayResearchQuestion]] = defaultdict(
                list[ImpactPathwayResearchQuestion]
            )
            for question in questions_by_cluster[i_cluster]:
                if question.time_frame in time_frame_column_numbers:
                    questions_per_time_frame_column[time_frame_column_numbers[question.time_frame]].append(question)

            columns: list[ClusterColumn] = []
            for i_column in questions_per_time_frame_column:
                questions_per_group_in_column: defaultdict[ResearchLine, list[ImpactPathwayResearchQuestion]] = defaultdict(
                    list[ImpactPathwayResearchQuestion]
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
                            title=self.translator.get_label(research_line.title),
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
