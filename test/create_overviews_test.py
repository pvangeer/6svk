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

from datetime import datetime

from svk.data._researchquestion import ResearchQuestion
from svk.data._timeframe import TimeFrame
from svk.io import KnowledgeAgendaDatabase
from svk.visualization import KnowledgeCalendarDocument
from svk.data import StormSurgeBarrier, Translator

base_dir = "C:/Users/geer/OneDrive - Stichting Deltares/Projecten/Kennisvragen SVK"
hv_dir = base_dir + "/03 HV/01 Uitwerking"
mlk_dir = base_dir + "/05 MLK/01 Uitwerking"
hk_dir = base_dir + "/06 HK/01 Uitwerking"
rp_dir = base_dir + "/07 RP/01 Uitwerking"
hijk_dir = base_dir + "/02 HIJK/01 Uitwerking"
esb_dir = base_dir + "/04 OSK/01 Uitwerking"


def read_database(file_path: str) -> list[ResearchQuestion]:
    questions = KnowledgeAgendaDatabase(file_path)
    questions.read()
    if len(questions.errors) > 0:
        for e in questions.errors:
            print(e)
    return [q for q in questions if q.time_frame != TimeFrame.NotRelevant]


def read_hv_database() -> list[ResearchQuestion]:
    return read_database(hv_dir + "/Eerste toepassing methodiek kennisvragen SVK HV_Concept.xlsx")


def read_mlk_database() -> list[ResearchQuestion]:
    return read_database(mlk_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK MLK.xlsx")


def read_hk_database() -> list[ResearchQuestion]:
    return read_database(hk_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK HK.xlsx")


def read_rp_database() -> list[ResearchQuestion]:
    return read_database(rp_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK RP.xlsx")


def read_hijk_database() -> list[ResearchQuestion]:
    return read_database(hijk_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK HIJK.xlsx")


def read_esb_database() -> list[ResearchQuestion]:
    return read_database(esb_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK OSK.xlsx")


def test_create_hv():
    barrier: StormSurgeBarrier = StormSurgeBarrier.HaringvlietBarrier
    questions = read_hv_database()
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


def test_create_mlk():
    questions = read_mlk_database()

    t = Translator(lang="nl")
    output_dir = "C:/Test/"  # mlk_dir
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda {t.get_label(StormSurgeBarrier.MaeslantBarrier.title)}"

    calendar = KnowledgeCalendarDocument(
        output_dir=output_dir,
        output_file=output_file,
        questions=questions,
        storm_surge_barrier=StormSurgeBarrier.MaeslantBarrier,
    )

    calendar.build()


def test_create_hk():
    questions = read_hk_database()
    t = Translator(lang="nl")
    output_dir = "C:/Test/"  # mlk_dir
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda {t.get_label(StormSurgeBarrier.HartelBarrier.title)}"

    calendar = KnowledgeCalendarDocument(
        output_dir=output_dir,
        output_file=output_file,
        questions=questions,
        storm_surge_barrier=StormSurgeBarrier.HartelBarrier,
    )

    calendar.build()


def test_create_rp():
    questions = read_rp_database()

    t = Translator(lang="nl")
    output_dir = "C:/Test/"  # rp_dir
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda {t.get_label(StormSurgeBarrier.Ramspol.title)}"

    calendar = KnowledgeCalendarDocument(
        output_dir=output_dir,
        output_file=output_file,
        questions=questions,
        storm_surge_barrier=StormSurgeBarrier.Ramspol,
    )

    calendar.build()


def test_create_hijk():
    questions = read_hijk_database()

    t = Translator(lang="nl")
    output_dir = "C:/Test/"  # rp_dir
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda {t.get_label(StormSurgeBarrier.HollandseIJsselBarrier.title)}"

    calendar = KnowledgeCalendarDocument(
        output_dir=output_dir,
        output_file=output_file,
        questions=questions,
        storm_surge_barrier=StormSurgeBarrier.HollandseIJsselBarrier,
    )

    calendar.build()


def test_create_esb():
    questions = read_esb_database()

    t = Translator(lang="nl")
    output_dir = "C:/Test/"  # esb_dir
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda {t.get_label(StormSurgeBarrier.EasternScheldtBarrier.title)}"

    calendar = KnowledgeCalendarDocument(
        output_dir=output_dir,
        output_file=output_file,
        questions=questions,
        storm_surge_barrier=StormSurgeBarrier.EasternScheldtBarrier,
    )

    calendar.build()


def test_create_complete_list():
    questions = read_hv_database() + read_rp_database() + read_mlk_database() + read_hijk_database() + read_hk_database()

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
