from svk.visualization import Figure, Group, Question, BarrierIcons, Column
from svk.data import TimeFrame, ResearchLines, ResearchQuestion, Priority, TimeFrame, ResearchLine
from svk.io import svg_to_pdf


def generate_research_question(question, time_frame, research_line: ResearchLine):
    generate_research_question.counter += 1
    return ResearchQuestion(
        id=f"T{str(generate_research_question.counter)}",
        question=question,
        storm_surge_barrier=["HV"],
        reference_ids=[],
        reference_question=generate_research_question.counter,
        prio_water_safety=Priority.Low,
        prio_management_maintenance=Priority.High,
        prio_other_functions=Priority.Medium,
        prio_operation=Priority.High,
        time_frame=time_frame,
        research_line_primary=research_line,
    )


generate_research_question.counter = 0


def test_create_image():
    fig = Figure(title="Test-image", barrier_icon=BarrierIcons.All)
    adaptation_now = Group(title="test", color="black", number=1)
    adaptation_now.questions.append(
        Question(
            research_question=generate_research_question(
                question="This is my first question", time_frame=TimeFrame.Now, research_line=ResearchLines.Adaptation.value
            )
        )
    )
    adaptation_now.questions.append(
        Question(
            research_question=generate_research_question(
                question="This is my second question", time_frame=TimeFrame.Now, research_line=ResearchLines.Adaptation.value
            )
        )
    )
    adaptation_now.questions.append(
        Question(
            research_question=generate_research_question(
                question="Now we try to pose a rediculous long question to see if outlines still match and all sizes and placement is correct. I will not stop trying until I get this right.",
                time_frame=TimeFrame.Now,
                research_line=ResearchLines.Adaptation.value,
            )
        )
    )
    fig.columns.append(Column(header_title="test", header_sub_title="sub 1", header_color="#07583753"))
    fig.columns[0].groups.append(adaptation_now)

    cyber_near = Group(
        title="test",
        color="blue",
        number=2,
    )
    cyber_near.questions.append(
        Question(
            research_question=generate_research_question(
                question="This is my first question", time_frame=TimeFrame.NearFuture, research_line=ResearchLines.Cyber.value
            )
        )
    )
    cyber_near.questions.append(
        Question(
            research_question=generate_research_question(
                question="This is my second question", time_frame=TimeFrame.NearFuture, research_line=ResearchLines.Cyber.value
            )
        )
    )
    cyber_near.questions.append(
        Question(
            research_question=generate_research_question(
                question="Now we try to pose a rediculous long question to see if outlines still match and all sizes and placement is correct. I will not stop trying until I get this right.",
                time_frame=TimeFrame.NearFuture,
                research_line=ResearchLines.Cyber.value,
            )
        )
    )
    fig.columns.append(Column(header_title="test", header_sub_title="sub 1", header_color="#478956"))
    fig.columns[1].groups.append(cyber_near)

    adaptation_near = Group(
        title="test",
        color="blue",
        number=2,
    )
    adaptation_near.questions.append(
        Question(
            research_question=generate_research_question(
                question="This is my first question", time_frame=TimeFrame.NearFuture, research_line=ResearchLines.Adaptation.value
            )
        )
    )
    adaptation_near.questions.append(
        Question(
            research_question=generate_research_question(
                question="This is my second question", time_frame=TimeFrame.NearFuture, research_line=ResearchLines.Adaptation.value
            )
        )
    )
    adaptation_near.questions.append(
        Question(
            research_question=generate_research_question(
                question="Now we try to pose a rediculous long question to see if outlines still match and all sizes and placement is correct. I will not stop trying until I get this right.",
                time_frame=TimeFrame.NearFuture,
                research_line=ResearchLines.Adaptation.value,
            )
        )
    )
    fig.columns[1].groups.append(adaptation_near)
    dwg = fig.draw()

    pt = "C:/test/Kennisagenda_auto.pdf"
    svg_to_pdf(dwg, pt)
