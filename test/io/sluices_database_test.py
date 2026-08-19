from svk.io._sluicesdatabase import SluicesKnowledgeAgendaDatabase
from svk.data import Priority, TimeFrame
from test.paths import test_data_dir


def test_read_sluices_database():
    """
    Test function for the sluices database. It reads the database file and prints the data.
    """

    d = SluicesKnowledgeAgendaDatabase(test_data_dir + "/example_sp.xlsx")
    d.read()
    assert d is not None
    assert len(d) > 65
    q = d[0]
    assert q.id == "SP_C1"
    assert q.sluice == "SP"  # TODO: Adjust to sluices
    assert q.question.startswith("Hoe bepaal je de kwaliteit en variabiliteit van het historische")
    assert q.prio_water_safety == Priority.Low
    assert q.prio_water_availability == Priority.Medium
    assert q.prio_shipping == Priority.Medium
    assert q.prio_other_functions == Priority.Low
    assert q.prio_management_maintenance == Priority.High
    assert q.prio_operation == Priority.Low
    assert q.time_frame == TimeFrame.Now
    assert q.research_line is not None
    assert q.research_line.number == 1
    assert q.contributes_to_standardisation
