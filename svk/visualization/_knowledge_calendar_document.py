from collections import defaultdict
from typing import DefaultDict
from pydantic import model_validator

from svk.data import ResearchQuestion, StormSurgeBarrier, TimeFrame, ResearchLine
from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.helpers._greyfraction import color_toward_grey
from svk.visualization.helpers import _calendar_helper as helper
from svk.visualization._time_line_overview_page import TimeLineOverviewPage
from svk.visualization._column import Column
from svk.visualization._group import Group
from svk.visualization._cluster import Cluster
from svk.visualization._question import Question
from svk.visualization._document import Document
from svk.visualization._page import Page


class KnowledgeCalendarDocument(Document):
    storm_surge_barrier: StormSurgeBarrier
    _clusters: dict[int, Cluster] = {}

    @model_validator(mode="before")
    @classmethod
    def set_defaults(cls, data):
        data["disclaimer"] = (
            "Dit is een eerste concept van de onderzoeksagenda stormvloedkeringen. Deze versie is ontstaan in samenwerking met de asset management teams van de keringen. De prioritering van de onderzoeksvragen moet nog gereviewd worden door o.a. de asset management teams en RWS WVL/GPO. De indeling in tijdsperiode is op dit moment in ontwikkeling. Voor vragen, neem contact op met Marit de Jong of Riva de Vries."
        )
        data["disclaimer_links"] = [
            ("Riva de Vries", "mailto:riva.de.vries@rws.nl"),
            ("Marit de Jong", "mailto:marit.de.jong@rws.nl"),
        ]

        return data

    def create_pages(self) -> list[Page]:
        return [self._create_overview_page(page_number=0)] + self.create_detailes_pages(current_page_number=1)

    def _create_overview_page(
        self,
        page_number: int,
    ) -> TimeLineOverviewPage:
        time_groups = defaultdict(list[ResearchQuestion])

        for q in self.questions:
            time_groups[q.time_frame].append(q)

        self.layout_configuration.question_id_box_width = (
            max([measure_text(q.id, self.layout_configuration.font_size)[0] for q in self.questions])
            + self.layout_configuration.small_margin
        )

        fig = TimeLineOverviewPage(
            page_number=page_number,
            title=self.translator.get_label(self.storm_surge_barrier.title),
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            icon=self.storm_surge_barrier,
            disclaimer=self.disclaimer,
            disclaimer_links=self.disclaimer_links,
        )
        self.add_time_frame_column(fig=fig, questions=time_groups[TimeFrame.Now], time_frame=TimeFrame.Now, number=0)
        self.add_time_frame_column(fig=fig, questions=time_groups[TimeFrame.NearFuture], time_frame=TimeFrame.NearFuture, number=1)
        self.add_time_frame_column(fig=fig, questions=time_groups[TimeFrame.Future], time_frame=TimeFrame.Future, number=2)
        fig.clusters = list(self._clusters.values())
        return fig

    def add_time_frame_column(self, fig: TimeLineOverviewPage, questions: list[ResearchQuestion], time_frame: TimeFrame, number: int):
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
