import pytest
from typing import cast
from datetime import datetime

from svk.data import StormSurgeBarrier, Translator, ResearchQuestion, ImpactPathwayResearchQuestion, TimeFrame
from svk.io import KnowledgeAgendaDatabase, ImpactPathwayDatabase
from svk.visualization import KnowledgeCalendarDocument, ImpactPathwayDocument

base_dir = "C:/Users/geer/OneDrive - Stichting Deltares/Projecten/Kennisvragen SVK"
hv_dir = base_dir + "/03 HV/01 Uitwerking"
mlk_dir = base_dir + "/05 MLK/01 Uitwerking"
hk_dir = base_dir + "/06 HK/01 Uitwerking"
rp_dir = base_dir + "/07 RP/01 Uitwerking"
hijk_dir = base_dir + "/02 HIJK/01 Uitwerking"
esb_dir = base_dir + "/04 OSK/01 Uitwerking"
allsvk_dir = base_dir + "/08 6SVK"
ssb_dir = "C:/Users/geer/OneDrive - Stichting Deltares/Projecten/11212142 - NWO SSB Delta/General/C. Report - advise/Impact pathway and research agenda"


def read_hv_database() -> list[ResearchQuestion]:
    questions = KnowledgeAgendaDatabase(hv_dir + "/Eerste toepassing methodiek kennisvragen SVK HV_Concept.xlsx")
    questions.read()
    return [q for q in questions if q.time_frame != TimeFrame.NotRelevant]


def read_mlk_database() -> list[ResearchQuestion]:
    questions = KnowledgeAgendaDatabase(mlk_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK MLK.xlsx")
    questions.read()
    return [q for q in questions if q.time_frame != TimeFrame.NotRelevant]


def read_hk_database() -> list[ResearchQuestion]:
    questions = KnowledgeAgendaDatabase(hk_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK HK.xlsx")
    questions.read()
    return [q for q in questions if q.time_frame != TimeFrame.NotRelevant]


def read_rp_database() -> list[ResearchQuestion]:
    questions = KnowledgeAgendaDatabase(rp_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK RP.xlsx")
    questions.read()
    return [q for q in questions if q.time_frame != TimeFrame.NotRelevant]


def read_hijk_database() -> list[ResearchQuestion]:
    questions = KnowledgeAgendaDatabase(hijk_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK HIJK.xlsx")
    questions.read()
    return [q for q in questions if q.time_frame != TimeFrame.NotRelevant]


def read_esb_database() -> list[ResearchQuestion]:
    questions = KnowledgeAgendaDatabase(esb_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK OSK.xlsx")
    questions.read()
    return [q for q in questions if q.time_frame != TimeFrame.NotRelevant]


def read_ssb_pathway_database() -> list[ImpactPathwayResearchQuestion]:
    d = ImpactPathwayDatabase(ssb_dir + "/SSB-delta_impact-pathway-database.xlsx")
    d.read()
    return [q for q in d if q.action_holder != "Not included"]


def get_output_file(barrier: StormSurgeBarrier, add: str | None = None) -> str:
    t = Translator(lang="nl")
    name = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda {t.get_label(barrier.title)}"
    if add is not None and add != "":
        name += f" - {add}"
    return name


# @pytest.mark.skip(reason="Use this to publish official version to correct output dir")
def test_create_hv():
    calendar = KnowledgeCalendarDocument(
        output_dir=hv_dir,
        output_file=get_output_file(StormSurgeBarrier.HaringvlietBarrier),
        questions=read_hv_database(),
        storm_surge_barrier=StormSurgeBarrier.HaringvlietBarrier,
    )
    calendar.build()


# @pytest.mark.skip(reason="Use this to publish official version to correct output dir")
def test_create_rp():
    calendar = KnowledgeCalendarDocument(
        output_dir=rp_dir,
        output_file=get_output_file(StormSurgeBarrier.Ramspol),
        questions=read_rp_database(),
        storm_surge_barrier=StormSurgeBarrier.Ramspol,
    )
    calendar.build()


# @pytest.mark.skip(reason="Use this to publish official version to correct output dir")
def test_create_hijk():
    calendar = KnowledgeCalendarDocument(
        output_dir=hijk_dir,
        output_file=get_output_file(StormSurgeBarrier.HollandseIJsselBarrier),
        questions=read_hijk_database(),
        storm_surge_barrier=StormSurgeBarrier.HollandseIJsselBarrier,
    )
    calendar.build()


# @pytest.mark.skip(reason="Use this to publish official version to correct output dir")
def test_create_mlk():
    calendar = KnowledgeCalendarDocument(
        output_dir=mlk_dir,
        output_file=get_output_file(StormSurgeBarrier.MaeslantBarrier),
        questions=read_mlk_database(),
        storm_surge_barrier=StormSurgeBarrier.MaeslantBarrier,
    )
    calendar.build()


# @pytest.mark.skip(reason="Use this to publish official version to correct output dir")
def test_create_hk():
    calendar = KnowledgeCalendarDocument(
        output_dir=hk_dir,
        output_file=get_output_file(StormSurgeBarrier.HartelBarrier),
        questions=read_hk_database(),
        storm_surge_barrier=StormSurgeBarrier.HartelBarrier,
    )
    calendar.build()


# @pytest.mark.skip(reason="Use this to publish official version to correct output dir")
def test_create_osk():
    calendar = KnowledgeCalendarDocument(
        output_dir=esb_dir,
        output_file=get_output_file(StormSurgeBarrier.EasternScheldtBarrier),
        questions=read_esb_database(),
        storm_surge_barrier=StormSurgeBarrier.EasternScheldtBarrier,
    )
    calendar.build()


# @pytest.mark.skip(reason="Use this to publish official version to correct output dir")
def test_create_6svk():
    all_questions = (
        read_hk_database()
        + read_hijk_database()
        + read_hv_database()
        + read_mlk_database()
        + read_rp_database()
        + read_esb_database()
        + read_ssb_pathway_database()
    )
    six_svk_questions = [q for q in all_questions if StormSurgeBarrier.All in q.storm_surge_barriers]
    calendar = KnowledgeCalendarDocument(
        output_dir=allsvk_dir,
        output_file=get_output_file(StormSurgeBarrier.All),
        questions=six_svk_questions,
        storm_surge_barrier=StormSurgeBarrier.All,
    )
    calendar.build()


# @pytest.mark.skip(reason="Use this to publish official version to correct output dir")
def test_create_all():
    calendar = KnowledgeCalendarDocument(
        output_dir=allsvk_dir,
        output_file=get_output_file(StormSurgeBarrier.All, "alle vragen"),
        questions=read_hk_database()
        + read_hijk_database()
        + read_hv_database()
        + read_mlk_database()
        + read_rp_database()
        + read_esb_database()
        + read_ssb_pathway_database(),
        storm_surge_barrier=StormSurgeBarrier.All,
    )
    calendar.build()


# @pytest.mark.skip(reason="Use this to publish official version to correct output dir")
def test_create_impact_pathway():
    questions = read_ssb_pathway_database()
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Impact pathway SSB-delta"

    pathway = ImpactPathwayDocument(
        questions=cast(list[ResearchQuestion], questions), output_dir=ssb_dir, output_file=output_file, cleanup=False
    )
    pathway.build()
