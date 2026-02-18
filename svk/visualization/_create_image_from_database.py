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

from svk.data import ResearchQuestion
from svk.io import svg_to_pdf, svg_to_pdf_chrome
from svk.data import TimeFrame, ResearchQuestion, ResearchLine, StormSurgeBarrier, LinksRegister
from svk.visualization._overview_page import OverviewPage
from svk.visualization._details_page import DetailsPage
from svk.visualization._question_details import QuestionDetails
from svk.visualization._column import Column
from svk.visualization._group import Group
from svk.visualization._question import Question
from svk.visualization._layout_configuration import LayoutConfiguration
from svk.visualization.helpers._greyfraction import color_toward_grey
from svk.visualization.helpers._measuretext import measure_text
from collections import defaultdict
from typing import DefaultDict


def get_priority(question: ResearchQuestion) -> int:
    return 1 if question.has_priority else 0


def get_column_title(time_frame: TimeFrame) -> str:
    match time_frame:
        case TimeFrame.Now:
            return "Nu"
        case TimeFrame.NearFuture:
            return "Nabije toekomst"
        case TimeFrame.Future:
            return "Toekomst"
        case TimeFrame.NotRelevant:
            return "Niet relevant"
        case TimeFrame.Unknown:
            return "Onbekend"
        case _:
            raise ValueError("Unknown time frame")


def get_subtitle(time_frame: TimeFrame) -> str:
    match time_frame:
        case TimeFrame.Now:
            return ""
        case TimeFrame.NearFuture:
            return "(2033 - 2040)"
        case TimeFrame.Future:
            return "(>2040)"
        case TimeFrame.NotRelevant:
            return "(-)"
        case TimeFrame.Unknown:
            return "(?)"
        case _:
            raise ValueError("Unknown time frame")


def get_header_color(time_frame: TimeFrame) -> str:
    return color_toward_grey((18, 103, 221), grey_fraction=time_frame.grey_fraction)


def add_column(config: LayoutConfiguration, links_manager: LinksRegister, fig: OverviewPage, time_groups, time_frame: TimeFrame):
    column = Column(
        layout_configuration=config,
        links_register=links_manager,
        header_title=get_column_title(time_frame),
        header_subtitle=get_subtitle(time_frame),
        header_color=get_header_color(time_frame),
    )

    filtered_questions = time_groups[time_frame]
    if len(filtered_questions) > 0:
        now_questions_groups: DefaultDict[ResearchLine, list[ResearchQuestion]] = defaultdict(list)
        for q in filtered_questions:
            now_questions_groups[q.research_line_primary].append(q)

        for group in sorted(now_questions_groups.keys(), key=lambda g: g.number):
            fig.layout_configuration.cluster_colors[group.cluster] = group.base_color
            column.groups[group.cluster] = Group(
                layout_configuration=config,
                links_register=links_manager,
                title=group.title,
                color=color_toward_grey(group.base_color, time_frame.grey_fraction),
            )
            for question in sorted(now_questions_groups[group], key=get_priority, reverse=True):
                column.groups[group.cluster].questions.append(
                    Question(layout_configuration=config, links_register=links_manager, research_question=question)
                )

        fig.columns.append(column)


def create_overview_page_from_questions(
    config: LayoutConfiguration,
    links_manager: LinksRegister,
    title: str,
    questions: list[ResearchQuestion],
    output_dir: str,
    file_name: str,
    storm_surge_barrier: StormSurgeBarrier,
):
    time_groups: DefaultDict[TimeFrame, list[ResearchQuestion]] = defaultdict(list[ResearchQuestion])

    for q in questions:
        time_groups[q.time_frame].append(q)

    config.question_id_box_width = max([measure_text(q.id, config.font_size)[0] for q in questions]) + config.line_margin

    fig = OverviewPage(
        page_number=0, layout_configuration=config, links_register=links_manager, title=title, storm_surge_barrier=storm_surge_barrier
    )
    add_column(config, links_manager=links_manager, fig=fig, time_groups=time_groups, time_frame=TimeFrame.Now)
    add_column(config, links_manager=links_manager, fig=fig, time_groups=time_groups, time_frame=TimeFrame.NearFuture)
    add_column(config, links_manager=links_manager, fig=fig, time_groups=time_groups, time_frame=TimeFrame.Future)
    dwg = fig.draw()
    return svg_to_pdf(dwg, output_dir, file_name)


def create_details_page_from_questions(
    config: LayoutConfiguration,
    links_manager: LinksRegister,
    questions: list[ResearchQuestion],
    title: str,
    output_dir: str,
    file_name: str,
):
    dwg_details_page = DetailsPage(page_number=1, layout_configuration=config, links_register=links_manager)
    for question in sorted(questions, key=lambda q: q.id):
        dwg_details_page.questions.append(
            QuestionDetails(layout_configuration=config, links_register=links_manager, research_question=question)
        )

    return svg_to_pdf(dwg=dwg_details_page.draw(), output_dir=output_dir, file_name=file_name)
