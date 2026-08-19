from datetime import datetime
from svk.data import SluicesResearchQuestion, TimeFrame, Translator, StormSurgeBarrier
from svk.io import SluicesKnowledgeAgendaDatabase
from svk.visualization import SluicesDocument
from test.paths import test_data_dir, test_output_dir


def read_database() -> list[SluicesResearchQuestion]:
    questions = SluicesKnowledgeAgendaDatabase(test_data_dir + "/example_sp.xlsx")
    questions.read()

    if len(questions.errors) > 0:
        for e in questions.errors:
            print(e)
    return [q for q in questions if q.time_frame != TimeFrame.NotRelevant]


def test_create_sluices_overview():
    questions = read_database()
    t = Translator(lang="nl")
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda Sluis Panheel"

    calendar = SluicesDocument(
        output_dir=test_output_dir,
        output_file=output_file,
        questions=questions,
    )

    calendar.build()
