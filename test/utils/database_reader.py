from pathlib import Path
from functools import cache
from svk.data import StormSurgeBarrier, StormSurgeBarrierResearchQuestion, ImpactPathwayResearchQuestion, TimeFrame, Grid
from svk.io import KnowledgeAgendaDatabase, EndOfLifeDatabase, ImpactPathwayDatabase

from test.paths import (
    mlk_database_path,
    hk_database_path,
    rp_database_path,
    hijk_database_path,
    hv_database_path,
    esb_database_path,
    ssb_database_path,
)


def get_database_dir(barrier: StormSurgeBarrier) -> Path:
    database_path = get_database_path(barrier=barrier)
    return database_path.parent if database_path.is_file() else database_path


def get_database_path(barrier: StormSurgeBarrier) -> Path:
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


@cache
def read_knowledge_agenda_database(barrier: StormSurgeBarrier) -> tuple[StormSurgeBarrierResearchQuestion, ...]:
    questions = KnowledgeAgendaDatabase(get_database_path(barrier=barrier))
    questions.read()
    if len(questions.errors) > 0:
        for e in questions.errors:
            print(e)
    return tuple(q for q in questions if q.time_frame != TimeFrame.NotRelevant)


@cache
def read_ssb_pathway_database() -> tuple[ImpactPathwayResearchQuestion, ...]:
    d = ImpactPathwayDatabase(ssb_database_path)
    d.read()
    if len(d.errors) > 0:
        for e in d.errors:
            print(e)
    return tuple(q for q in d if q.action_holder != "Not included")


@cache
def read_end_of_life_database(
    barrier: StormSurgeBarrier, row_header_column: int, row_header_categories_column: int, sheet_name: str
) -> Grid:
    d = EndOfLifeDatabase(file_path=get_database_path(barrier=barrier))
    d.sheet_name = sheet_name
    d.row_header_column = row_header_column
    d.row_header_categories_column = row_header_categories_column
    d.read()
    assert d.grid is not None
    return d.grid
