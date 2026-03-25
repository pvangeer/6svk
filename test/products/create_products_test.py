import pytest
from typing import cast
from datetime import datetime

from svk.data import StormSurgeBarrier, Translator, ResearchQuestion
from svk.io import KnowledgeAgendaDatabase, ImpactPathwayDatabase
from svk.visualization import KnowledgeCalendarDocument, ImpactPathwayDocument

base_dir = "C:/Users/geer/OneDrive - Stichting Deltares/Projecten/Kennisvragen SVK"


@pytest.mark.skip(reason="Use this to publish official version to correct output dir")
def test_create_hv_calendar():
    hv_dir = base_dir + "/03 HV/01 Uitwerking"
    database_path = hv_dir + "/Eerste toepassing methodiek kennisvragen SVK HV_Concept.xlsx"
    t = Translator(lang="nl")
    output_dir = hv_dir
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda {t.get_label(StormSurgeBarrier.HaringvlietBarrier.title)}"

    questions = KnowledgeAgendaDatabase(database_path)
    questions.read()
    calendar = KnowledgeCalendarDocument(
        output_dir=output_dir,
        output_file=output_file,
        questions=questions,
        storm_surge_barrier=StormSurgeBarrier.HaringvlietBarrier,
    )

    calendar.build()


@pytest.mark.skip(reason="Use this to publish official version to correct output dir")
def test_create_rp():
    rp_dir = base_dir + "/07 RP/01 Uitwerking"
    database_path = rp_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK RP.xlsx"
    t = Translator(lang="nl")
    output_dir = rp_dir
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda {t.get_label(StormSurgeBarrier.Ramspol.title)}"

    questions = KnowledgeAgendaDatabase(database_path)
    questions.read()
    calendar = KnowledgeCalendarDocument(
        output_dir=output_dir,
        output_file=output_file,
        questions=questions,
        storm_surge_barrier=StormSurgeBarrier.Ramspol,
    )

    calendar.build()


@pytest.mark.skip(reason="Use this to publish official version to correct output dir")
def test_create_hijk():
    hijk_dir = base_dir + "/02 HIJK/01 Uitwerking"
    database_path = hijk_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK HIJK.xlsx"
    t = Translator(lang="nl")
    output_dir = hijk_dir
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda {t.get_label(StormSurgeBarrier.HollandseIJsselBarrier.title)}"

    questions = KnowledgeAgendaDatabase(database_path)
    questions.read()
    calendar = KnowledgeCalendarDocument(
        output_dir=output_dir,
        output_file=output_file,
        questions=questions,
        storm_surge_barrier=StormSurgeBarrier.HollandseIJsselBarrier,
    )

    calendar.build()


@pytest.mark.skip(reason="Use this to publish official version to correct output dir")
def test_create_impact_pathway():
    # TODO: Change output path once I have access tot the sharepoint site.
    impact_dir = "C:/Test/"
    database_path = impact_dir + "/SSB-delta_impact-pathway-database.xlsx"
    output_dir = impact_dir

    d = ImpactPathwayDatabase(database_path)
    d.read()
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Impact pathway SSB-delta"

    pathway = ImpactPathwayDocument(questions=cast(list[ResearchQuestion], d), output_dir=output_dir, output_file=output_file)
    pathway.build()
