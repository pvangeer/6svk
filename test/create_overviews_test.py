"""
Copyright (C) Stichting Deltares 2026. All rights reserved.

This file is part of the 6svk toolbox.

This program is free software; you can redistribute it and/or modify it under the terms of
the GNU Lesser General Public License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with this
program; if not, see <https://www.gnu.org/licenses/>.

All names, logos, and references to "Deltares" are registered trademarks of Stichting
Deltares and remain full property of Stichting Deltares at all times. All rights reserved.
"""

import pytest
from datetime import datetime

from svk.data import TimeFrame, ResearchQuestion, Translator
from svk.io import KnowledgeAgendaDatabase, EndOfLifeDatabase, svg_to_pdf_chrome
from svk.visualization import KnowledgeCalendarDocument, EndOfLifePage, LayoutConfiguration
from svk.data import StormSurgeBarrier, Translator, LinksRegister

base_dir = "C:/Users/geer/OneDrive - Stichting Deltares/Projecten/Kennisvragen SVK"
hv_dir = base_dir + "/03 HV/01 Uitwerking"
mlk_dir = base_dir + "/05 MLK/01 Uitwerking"
hk_dir = base_dir + "/06 HK/01 Uitwerking"
rp_dir = base_dir + "/07 RP/01 Uitwerking"
hijk_dir = base_dir + "/02 HIJK/01 Uitwerking"
esb_dir = base_dir + "/04 OSK/01 Uitwerking"

hv_database_path = hv_dir + "/Eerste toepassing methodiek kennisvragen SVK HV_Concept.xlsx"
mlk_database_path = mlk_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK MLK.xlsx"
hk_database_path = hk_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK HK.xlsx"
rp_database_path = rp_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK RP.xlsx"
hijk_database_path = hijk_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK HIJK.xlsx"
esb_database_path = esb_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK OSK.xlsx"


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
    if len(questions.errors) > 0:
        for e in questions.errors:
            print(e)
    return [q for q in questions if q.time_frame != TimeFrame.NotRelevant]


def test_create_hv():
    barrier: StormSurgeBarrier = StormSurgeBarrier.HaringvlietBarrier
    questions = read_database(barrier)
    t = Translator(lang="nl")
    output_dir = "C:/Test/"  # hv_dir
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda {t.get_label(barrier.title)}"

    calendar = KnowledgeCalendarDocument(
        output_dir=output_dir,
        output_file=output_file,
        questions=questions,
        storm_surge_barrier=barrier,
    )

    calendar.build()


@pytest.mark.parametrize(
    "barrier,row_header_column,row_header_categories_column",
    [
        pytest.param(StormSurgeBarrier.EasternScheldtBarrier, 1, 1, id=StormSurgeBarrier.EasternScheldtBarrier.title.value[0]),
        pytest.param(StormSurgeBarrier.MaeslantBarrier, 1, 1, id=StormSurgeBarrier.MaeslantBarrier.title.value[0]),
        pytest.param(StormSurgeBarrier.HartelBarrier, 1, 1, id=StormSurgeBarrier.HartelBarrier.title.value[0]),
        pytest.param(StormSurgeBarrier.HaringvlietBarrier, 2, 1, id=StormSurgeBarrier.HaringvlietBarrier.title.value[0]),
        pytest.param(StormSurgeBarrier.HollandseIJsselBarrier, 1, 1, id=StormSurgeBarrier.HollandseIJsselBarrier.title.value[0]),
        pytest.param(StormSurgeBarrier.Ramspol, 1, 1, id=StormSurgeBarrier.Ramspol.title.value[0]),
    ],
)
def test_create_efl(barrier: StormSurgeBarrier, row_header_column: int, row_header_categories_column: int):
    barrier_title = Translator(lang="nl").get_label(barrier.title)

    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - EFL {barrier_title}"
    d = EndOfLifeDatabase(file_path=get_database_path(barrier=barrier))
    d.row_header_column = row_header_column
    d.row_header_categories_column = row_header_categories_column
    d.read()
    assert d.grid is not None

    page = EndOfLifePage(
        page_number=0,
        title=f"EFL - {barrier_title}",
        icon=barrier,
        layout_configuration=LayoutConfiguration(),
        links_register=LinksRegister(),
        translator=Translator(),
        grid=d.grid,
    )
    dwg = page.draw()
    svg_to_pdf_chrome(dwg, "C:/Test/" + output_file + ".pdf")


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
def test_create_etl(barrier: StormSurgeBarrier):
    barrier_title = Translator(lang="nl").get_label(barrier.title)

    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - ETL {barrier_title}"
    d = EndOfLifeDatabase(file_path=get_database_path(barrier=barrier))
    d.sheet_name = "ETL"
    d.row_header_column = 1
    d.row_header_categories_column = 1
    d.read()
    assert d.grid is not None

    page = EndOfLifePage(
        page_number=0,
        title=f"ETL - {barrier_title}",
        icon=barrier,
        layout_configuration=LayoutConfiguration(),
        links_register=LinksRegister(),
        translator=Translator(),
        grid=d.grid,
    )
    dwg = page.draw()
    svg_to_pdf_chrome(dwg, "C:/Test/" + output_file + ".pdf")


def test_create_mlk():
    barrier = StormSurgeBarrier.MaeslantBarrier
    questions = read_database(barrier)

    t = Translator(lang="nl")
    output_dir = "C:/Test/"  # mlk_dir
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda {t.get_label(barrier.title)}"

    calendar = KnowledgeCalendarDocument(
        output_dir=output_dir,
        output_file=output_file,
        questions=questions,
        storm_surge_barrier=barrier,
    )

    calendar.build()


def test_create_hk():
    barrier = StormSurgeBarrier.HartelBarrier
    questions = read_database(barrier)
    t = Translator(lang="nl")
    output_dir = "C:/Test/"  # mlk_dir
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda {t.get_label(barrier.title)}"

    calendar = KnowledgeCalendarDocument(
        output_dir=output_dir,
        output_file=output_file,
        questions=questions,
        storm_surge_barrier=barrier,
    )

    calendar.build()


def test_create_rp():
    barrier = StormSurgeBarrier.Ramspol
    questions = read_database(barrier)

    t = Translator(lang="nl")
    output_dir = "C:/Test/"  # rp_dir
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda {t.get_label(barrier.title)}"

    calendar = KnowledgeCalendarDocument(
        output_dir=output_dir,
        output_file=output_file,
        questions=questions,
        storm_surge_barrier=barrier,
    )

    calendar.build()


def test_create_hijk():
    barrier = StormSurgeBarrier.HollandseIJsselBarrier
    questions = read_database(barrier)

    t = Translator(lang="nl")
    output_dir = "C:/Test/"  # rp_dir
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda {t.get_label(barrier.title)}"

    calendar = KnowledgeCalendarDocument(
        output_dir=output_dir,
        output_file=output_file,
        questions=questions,
        storm_surge_barrier=barrier,
    )

    calendar.build()


def test_create_esb():
    barrier = StormSurgeBarrier.EasternScheldtBarrier
    questions = read_database(barrier)

    t = Translator(lang="nl")
    output_dir = "C:/Test/"  # esb_dir
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda {t.get_label(barrier.title)}"

    calendar = KnowledgeCalendarDocument(
        output_dir=output_dir,
        output_file=output_file,
        questions=questions,
        storm_surge_barrier=barrier,
    )

    calendar.build()


def test_create_complete_list():
    questions = (
        read_database(StormSurgeBarrier.HaringvlietBarrier)
        + read_database(StormSurgeBarrier.Ramspol)
        + read_database(StormSurgeBarrier.MaeslantBarrier)
        + read_database(StormSurgeBarrier.HartelBarrier)
        + read_database(StormSurgeBarrier.HollandseIJsselBarrier)
        + read_database(StormSurgeBarrier.EasternScheldtBarrier)
    )

    t = Translator(lang="nl")
    output_dir = "C:/Test/"
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda compleet 6SVK"

    calendar = KnowledgeCalendarDocument(
        output_dir=output_dir,
        output_file=output_file,
        questions=questions,
        storm_surge_barrier=StormSurgeBarrier.All,
    )

    calendar.build()
