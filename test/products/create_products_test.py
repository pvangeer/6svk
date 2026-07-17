import pytest
from typing import cast
from datetime import datetime

from svk.data import StormSurgeBarrier, Translator, ResearchQuestion, ImpactPathwayResearchQuestion, TimeFrame, Grid
from svk.io import KnowledgeAgendaDatabase, ImpactPathwayDatabase, EndOfLifeDatabase
from svk.visualization import (
    KnowledgeCalendarDocument,
    ImpactPathwayDocument,
    LifeTimeAnalysDocument,
    CustomPagesDocument,
    LifeTimeAnalysisPage,
)

base_dir = "C:/Users/geer/OneDrive - Stichting Deltares/Projecten/Kennisvragen SVK"
hv_dir = base_dir + "/03 HV/01 Uitwerking"
mlk_dir = base_dir + "/05 MLK/01 Uitwerking"
hk_dir = base_dir + "/06 HK/01 Uitwerking"
rp_dir = base_dir + "/07 RP/01 Uitwerking"
hijk_dir = base_dir + "/02 HIJK/01 Uitwerking"
esb_dir = base_dir + "/04 OSK/01 Uitwerking"
allsvk_dir = base_dir + "/08 6SVK"
ssb_dir = "C:/Users/geer/OneDrive - Stichting Deltares/Projecten/11212142 - NWO SSB Delta/General/C. Report - advise/Impact pathway and research agenda"

hv_database_path = hv_dir + "/Eerste toepassing methodiek kennisvragen SVK HV_Concept.xlsx"
mlk_database_path = mlk_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK MLK.xlsx"
hk_database_path = hk_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK HK.xlsx"
rp_database_path = rp_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK RP.xlsx"
hijk_database_path = hijk_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK HIJK.xlsx"
esb_database_path = esb_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK OSK.xlsx"
ssb_database_path = ssb_dir + "/SSB-delta_impact-pathway-database.xlsx"


def get_output_path(barrier: StormSurgeBarrier) -> str:
    match barrier:
        case StormSurgeBarrier.MaeslantBarrier:
            return mlk_dir
        case StormSurgeBarrier.HartelBarrier:
            return hk_dir
        case StormSurgeBarrier.Ramspol:
            return rp_dir
        case StormSurgeBarrier.HollandseIJsselBarrier:
            return hijk_dir
        case StormSurgeBarrier.HaringvlietBarrier:
            return hv_dir
        case StormSurgeBarrier.EasternScheldtBarrier:
            return esb_dir
        case _:
            raise


def get_database_path(barrier: StormSurgeBarrier) -> str:
    match barrier:
        case StormSurgeBarrier.MaeslantBarrier:
            return mlk_database_path
        case StormSurgeBarrier.HartelBarrier:
            return hk_database_path
        case StormSurgeBarrier.Ramspol:
            return rp_database_path
        case StormSurgeBarrier.HollandseIJsselBarrier:
            return hijk_database_path
        case StormSurgeBarrier.HaringvlietBarrier:
            return hv_database_path
        case StormSurgeBarrier.EasternScheldtBarrier:
            return esb_database_path
        case _:
            raise


def read_database(barrier: StormSurgeBarrier) -> list[ResearchQuestion]:
    questions = KnowledgeAgendaDatabase(get_database_path(barrier=barrier))
    questions.read()
    return [q for q in questions if q.time_frame != TimeFrame.NotRelevant]


def read_efl(barrier: StormSurgeBarrier) -> Grid:
    d = EndOfLifeDatabase(file_path=get_database_path(barrier=barrier))
    d.sheet_name = "EFL"
    d.row_header_column = 2 if barrier == StormSurgeBarrier.HaringvlietBarrier else 1
    d.row_header_categories_column = 1
    d.read()
    assert d.grid is not None
    return d.grid


def read_etl(barrier: StormSurgeBarrier) -> Grid:
    d = EndOfLifeDatabase(file_path=get_database_path(barrier=barrier))
    d.sheet_name = "ETL"
    d.row_header_column = 1
    d.row_header_categories_column = 1
    d.read()
    assert d.grid is not None
    return d.grid


def read_ssb_pathway_database() -> list[ImpactPathwayResearchQuestion]:
    d = ImpactPathwayDatabase(ssb_database_path)
    d.read()
    return [q for q in d if q.action_holder != "Not included"]


def get_knowledge_calendar_output_file(barrier: StormSurgeBarrier, add: str | None = None) -> str:
    t = Translator(lang="nl")
    name = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda {t.get_label(barrier.title)}"
    if add is not None and add != "":
        name += f" - {add}"
    return name


# @pytest.mark.skip(reason="Use this to publish official version to correct output dir")
@pytest.mark.parametrize(
    "barrier",
    [
        pytest.param(StormSurgeBarrier.EasternScheldtBarrier, id=StormSurgeBarrier.EasternScheldtBarrier.title.value[0]),
        pytest.param(StormSurgeBarrier.MaeslantBarrier, id=StormSurgeBarrier.MaeslantBarrier.title.value[0]),
        pytest.param(StormSurgeBarrier.HartelBarrier, id=StormSurgeBarrier.HartelBarrier.title.value[0]),
        pytest.param(StormSurgeBarrier.HaringvlietBarrier, id=StormSurgeBarrier.HaringvlietBarrier.title.value[0]),
        pytest.param(StormSurgeBarrier.HollandseIJsselBarrier, id=StormSurgeBarrier.HollandseIJsselBarrier.title.value[0]),
        pytest.param(StormSurgeBarrier.Ramspol, id=StormSurgeBarrier.Ramspol.title.value[0]),
    ],
)
def test_create_knowledge_calendar_per_ssb(barrier: StormSurgeBarrier):
    calendar_document = KnowledgeCalendarDocument(
        output_dir=get_output_path(barrier=barrier),
        output_file=get_knowledge_calendar_output_file(barrier=barrier),
        questions=read_database(barrier=barrier),
        storm_surge_barrier=barrier,
    )
    calendar_document.build()


# @pytest.mark.skip(reason="Use this to publish official version to correct output dir")
def test_create_6svk():
    all_questions = (
        read_database(StormSurgeBarrier.HartelBarrier)
        + read_database(StormSurgeBarrier.HollandseIJsselBarrier)
        + read_database(StormSurgeBarrier.HaringvlietBarrier)
        + read_database(StormSurgeBarrier.MaeslantBarrier)
        + read_database(StormSurgeBarrier.Ramspol)
        + read_database(StormSurgeBarrier.EasternScheldtBarrier)
        + read_ssb_pathway_database()
    )
    six_svk_questions = [q for q in all_questions if StormSurgeBarrier.All in q.storm_surge_barriers]
    calendar = KnowledgeCalendarDocument(
        output_dir=allsvk_dir,
        output_file=get_knowledge_calendar_output_file(StormSurgeBarrier.All),
        questions=six_svk_questions,
        storm_surge_barrier=StormSurgeBarrier.All,
    )
    calendar.build()


# @pytest.mark.skip(reason="Use this to publish official version to correct output dir")
def test_create_all():
    calendar = KnowledgeCalendarDocument(
        output_dir=allsvk_dir,
        output_file=get_knowledge_calendar_output_file(StormSurgeBarrier.All, "alle vragen"),
        questions=read_database(StormSurgeBarrier.HartelBarrier)
        + read_database(StormSurgeBarrier.HollandseIJsselBarrier)
        + read_database(StormSurgeBarrier.HaringvlietBarrier)
        + read_database(StormSurgeBarrier.MaeslantBarrier)
        + read_database(StormSurgeBarrier.Ramspol)
        + read_database(StormSurgeBarrier.EasternScheldtBarrier)
        + read_ssb_pathway_database(),
        storm_surge_barrier=StormSurgeBarrier.All,
    )
    calendar.build()


# @pytest.mark.skip(reason="Use this to publish official version to correct output dir")
@pytest.mark.parametrize(
    "barrier",
    [
        pytest.param(StormSurgeBarrier.EasternScheldtBarrier, id=StormSurgeBarrier.EasternScheldtBarrier.title.value[0]),
        pytest.param(StormSurgeBarrier.MaeslantBarrier, id=StormSurgeBarrier.MaeslantBarrier.title.value[0]),
        pytest.param(StormSurgeBarrier.HartelBarrier, id=StormSurgeBarrier.HartelBarrier.title.value[0]),
        pytest.param(StormSurgeBarrier.HaringvlietBarrier, id=StormSurgeBarrier.HaringvlietBarrier.title.value[0]),
        pytest.param(StormSurgeBarrier.HollandseIJsselBarrier, id=StormSurgeBarrier.HollandseIJsselBarrier.title.value[0]),
        pytest.param(StormSurgeBarrier.Ramspol, id=StormSurgeBarrier.Ramspol.title.value[0]),
    ],
)
def test_create_end_of_life_analysis_document(barrier: StormSurgeBarrier):
    document = LifeTimeAnalysDocument(
        storm_surge_barrier=barrier,
        functional_lifetime_grid=read_efl(barrier=barrier),
        technical_lifetime_grid=read_etl(barrier=barrier),
        output_dir=get_output_path(barrier=barrier),
        output_file=f"{datetime.now().strftime("%Y-%m-%d")} - Einde levensduur analyse {Translator(lang="nl").get_label(barrier.title)}",
    )
    document.build()


def test_create_end_of_life_time_summary():
    pages = []
    page_count = 0
    document = CustomPagesDocument(
        output_dir=allsvk_dir,
        output_file=f"{datetime.now().strftime("%Y-%m-%d")} - Einde levensduur analyse",
        custom_pages=pages,
    )
    for barrier in [
        StormSurgeBarrier.MaeslantBarrier,
        StormSurgeBarrier.HartelBarrier,
        StormSurgeBarrier.HaringvlietBarrier,
        StormSurgeBarrier.EasternScheldtBarrier,
        StormSurgeBarrier.HollandseIJsselBarrier,
        StormSurgeBarrier.Ramspol,
    ]:
        pages.append(
            LifeTimeAnalysisPage(
                page_number=page_count,
                title=f"EFL - {document.translator.get_label(barrier.title)}",
                layout_configuration=document.layout_configuration,
                links_register=document.links_register,
                translator=document.translator,
                icon=barrier,
                disclaimer=document.disclaimer,
                disclaimer_links=document.disclaimer_links,
                grid=read_efl(barrier=barrier),
            )
        )
        page_count += 1
        pages.append(
            LifeTimeAnalysisPage(
                page_number=page_count,
                title=f"ETL - {document.translator.get_label(barrier.title)}",
                layout_configuration=document.layout_configuration,
                links_register=document.links_register,
                translator=document.translator,
                icon=barrier,
                disclaimer=document.disclaimer,
                disclaimer_links=document.disclaimer_links,
                grid=read_etl(barrier=barrier),
            )
        )
        page_count += 1
    document.custom_pages = pages
    document.build()


@pytest.mark.skip(reason="Use this to publish official version to correct output dir")
def test_create_impact_pathway():
    questions = read_ssb_pathway_database()
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Impact pathway SSB-delta"

    pathway = ImpactPathwayDocument(
        questions=cast(list[ResearchQuestion], questions), output_dir=ssb_dir, output_file=output_file, cleanup=False
    )
    pathway.build()
