from collections import defaultdict
from typing import cast
from pydantic import model_validator
from svk.data import ImpactPathwayResearchQuestion, StormSurgeBarrier, TimeFrame, ResearchLine, ImpactCategory
from svk.visualization.pages._page import Page
from svk.visualization.helpers import _calendar_helper as helper
from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.helpers._greyfraction import color_toward_grey
from svk.visualization.pages._time_line_overview_page import TimeLineOverviewPage
from svk.visualization.elements._column import Column
from svk.visualization.elements._group import Group, PlainTextGroup
from svk.visualization.elements._cluster import Cluster
from svk.visualization.elements._question import Question
from svk.visualization.documents._document import Document
from datetime import date


class ImpactPathwayDocument(Document):
    @model_validator(mode="before")
    @classmethod
    def set_defaults(cls, data):
        data["disclaimer"] = (
            f"This is the impact pathway of the NWO SSB-∆ project (version 0.9 - {date.today()}). For questions, please contact Esther van Baaren or Bram van Prooijen."
        )
        data["disclaimer_links"] = [
            ("Esther van Baaren", "mailto:esther.vanbaaren@deltares.nl"),
            ("Bram van Prooijen", "mailto:b.c.vanprooijen@tudelft.nl"),
        ]

        return data

    def create_pages(self) -> list[Page]:
        return [self._create_overview_page(page_number=0)] + self.create_detailes_pages(current_page_number=1)

    def _create_overview_page(
        self,
        page_number: int,
    ) -> TimeLineOverviewPage:
        self.layout_configuration.question_id_box_width = (
            max([measure_text(q.id, self.layout_configuration.font_size)[0] for q in self.questions])
            + self.layout_configuration.small_margin
        )

        fig = TimeLineOverviewPage(
            page_number=page_number,
            title="Impact pathway",
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            icon=StormSurgeBarrier.All,
            disclaimer=self.disclaimer,
            disclaimer_links=self.disclaimer_links,
        )
        self.add_time_frame_column(fig=fig, time_frame=TimeFrame.Now, number=0)
        self.add_time_frame_column(fig=fig, time_frame=TimeFrame.NearFuture, number=1)
        self.add_time_frame_column(fig=fig, time_frame=TimeFrame.Future, number=2)
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

        self.add_clusters(fig=fig, questions=cast(list[ImpactPathwayResearchQuestion], self.questions))

        return fig

    def add_clusters(self, fig: TimeLineOverviewPage, questions: list[ImpactPathwayResearchQuestion]):
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
