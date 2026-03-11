from collections import defaultdict
from typing import DefaultDict

from svk.data import ResearchQuestion, StormSurgeBarrier, TimeFrame, ResearchLine
from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.helpers._greyfraction import color_toward_grey
from svk.visualization.helpers import _calendar_helper as helper
from svk.visualization._overview_page import OverviewPage
from svk.visualization._column import Column
from svk.visualization._group import Group
from svk.visualization._cluster import Cluster
from svk.visualization._question import Question
from svk.visualization._main_visualization_container import MainVisualizationContainer


class KnowledgeCalendar(MainVisualizationContainer):
    storm_surge_barrier: StormSurgeBarrier
    _clusters: dict[int, Cluster] = {}

    def create_overview_page(
        self,
        page_number: int,
    ) -> OverviewPage:
        time_groups = defaultdict(list[ResearchQuestion])

        for q in self.questions:
            time_groups[q.time_frame].append(q)

        self.layout_configuration.question_id_box_width = (
            max([measure_text(q.id, self.layout_configuration.font_size)[0] for q in self.questions])
            + self.layout_configuration.small_margin
        )

        fig = OverviewPage(
            page_number=page_number,
            title=self.translator.get_label(self.storm_surge_barrier.title),
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            storm_surge_barrier=self.storm_surge_barrier,
        )
        self.add_time_frame_column(fig=fig, questions=time_groups[TimeFrame.Now], time_frame=TimeFrame.Now, number=0)
        self.add_time_frame_column(fig=fig, questions=time_groups[TimeFrame.NearFuture], time_frame=TimeFrame.NearFuture, number=1)
        self.add_time_frame_column(fig=fig, questions=time_groups[TimeFrame.Future], time_frame=TimeFrame.Future, number=2)
        fig.clusters = list(self._clusters.values())
        return fig

    def add_time_frame_column(self, fig: OverviewPage, questions: list[ResearchQuestion], time_frame: TimeFrame, number: int):
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
                    # TODO: This should not occur here. Look at impact pathway for solution (build rows instead of columns)
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
