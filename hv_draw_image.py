from svk.io import Database, svg_to_pdf
from svk.data import TimeFrame, ResearchQuestion
from svk.visualization import Figure, Column, Group, Question
from collections import defaultdict


hv_questions = Database("C:/src/6svk/examples/Example-HV.xlsx")
hv_questions.read()
for e in hv_questions.errors:
    print(f"{e.cell_reference}: {str(e)}")

time_groups = defaultdict(list[ResearchQuestion])
for q in hv_questions:
    time_groups[q.time_frame].append(q)


def get_priority(question: Question) -> int:
    return 1 if question.high_priority else 0


def add_column(fig: Figure, time_groups, time_frame: TimeFrame):
    column = Column(time_frame=time_frame, groups=[])

    filtered_questions = time_groups[time_frame]
    if len(filtered_questions) > 0:
        now_questions_groups = defaultdict(list[ResearchQuestion])
        for q in filtered_questions:
            now_questions_groups[q.research_line_primary].append(q)

        for group in sorted(now_questions_groups.keys(), key=lambda g: g.number):
            column.groups.append(
                Group(
                    time_frame=time_frame,
                    research_line=group,
                    questions=sorted([Question(research_question=q) for q in now_questions_groups[group]], key=get_priority, reverse=True),
                )
            )

        fig.columns.append(column)


fig = Figure(columns=[])
add_column(fig=fig, time_groups=time_groups, time_frame=TimeFrame.Now)
add_column(fig=fig, time_groups=time_groups, time_frame=TimeFrame.NearFuture)
add_column(fig=fig, time_groups=time_groups, time_frame=TimeFrame.Future)
dwg = fig.draw()
svg_to_pdf(dwg, "C:/Test/HV-kennisvragen.pdf")
