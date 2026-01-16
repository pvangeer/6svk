from svk.visualization import Figure, Group, Question
from svk.data import TimeFrame, ResearchLines, ResearchQuestion, Priority, TimeFrame, ResearchLine
from svk.io import svg_to_pdf


def generate_research_question(question, time_frame, research_line: ResearchLine):
    generate_research_question.counter += 1
    return ResearchQuestion(
        question=question,
        storm_surge_barrier=["HV"],
        reference_codes=[f"T{str(generate_research_question.counter)}"],
        reference_number=generate_research_question.counter,
        prio_water_safety=Priority.Low,
        prio_budget=Priority.High,
        prio_functions=Priority.Medium,
        prio_operation=Priority.High,
        time_frame=time_frame,
        research_line_primary=research_line,
    )


generate_research_question.counter = 0


def test_create_image():
    fig = Figure()
    adaptation_now = Group(time_frame=TimeFrame.Now, research_line=ResearchLines.Adaptation.value, base_color=(237, 113, 39))
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
    fig.columns[0].groups.append(adaptation_now)

    cyber_near = Group(time_frame=TimeFrame.NearFuture, research_line=ResearchLines.Cyber.value, base_color=(237, 113, 39))
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
    fig.columns[1].groups.append(cyber_near)

    adaptation_near = Group(time_frame=TimeFrame.NearFuture, research_line=ResearchLines.Cyber.value, base_color=(237, 113, 39))
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
