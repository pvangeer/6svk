from svk.data import ResearchQuestion
from svk.io import svg_to_pdf
from svk.data import TimeFrame, ResearchQuestion, ResearchLine
from svk.visualization._figure import Figure
from svk.visualization._column import Column
from svk.visualization._group import Group
from svk.visualization._question import Question
from svk.visualization.helpers._greyfraction import color_toward_grey
from svk.visualization.helpers.icons._icons import BarrierIcons
from collections import defaultdict
from typing import DefaultDict


def get_priority(question: Question) -> int:
    return 1 if question.high_priority else 0


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


def get_sub_title(time_frame: TimeFrame) -> str:
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


def add_column(fig: Figure, time_groups, time_frame: TimeFrame):
    column = Column(
        header_title=get_column_title(time_frame),
        header_sub_title=get_sub_title(time_frame),
        header_color=get_header_color(time_frame),
        groups=[],
    )

    filtered_questions = time_groups[time_frame]
    if len(filtered_questions) > 0:
        now_questions_groups: DefaultDict[ResearchLine, list[ResearchQuestion]] = defaultdict(list)
        for q in filtered_questions:
            now_questions_groups[q.research_line_primary].append(q)

        for group in sorted(now_questions_groups.keys(), key=lambda g: g.number):
            column.groups.append(
                Group(
                    title=group.title,
                    color=color_toward_grey(group.base_color, time_frame.grey_fraction),
                    number=group.color_group,
                    questions=sorted([Question(research_question=q) for q in now_questions_groups[group]], key=get_priority, reverse=True),
                )
            )

        fig.columns.append(column)


def create_image_from_database(title: str, database: list[ResearchQuestion], output_file_path: str, barrier_icon: BarrierIcons):
    time_groups = defaultdict(list[ResearchQuestion])

    for q in database:
        time_groups[q.time_frame].append(q)

    fig = Figure(title=title, barrier_icon=barrier_icon, columns=[])
    add_column(fig=fig, time_groups=time_groups, time_frame=TimeFrame.Now)
    add_column(fig=fig, time_groups=time_groups, time_frame=TimeFrame.NearFuture)
    add_column(fig=fig, time_groups=time_groups, time_frame=TimeFrame.Future)
    dwg = fig.draw()
    svg_to_pdf(dwg, output_file_path)
