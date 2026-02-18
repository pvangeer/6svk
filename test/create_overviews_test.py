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

from svk.io import Database
from svk.visualization import KnowledgeCalendar
from svk.data import StormSurgeBarrier

base_dir = "C:/Users/geer/OneDrive - Stichting Deltares/Projecten/Kennisvragen SVK"


def test_create_hv():
    hv_dir = base_dir + "/03 HV/01 Uitwerking"
    database_path = hv_dir + "/Eerste toepassing methodiek kennisvragen SVK HV_Concept.xlsx"
    output_dir = "C:/Test/"  # hv_dir
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda {StormSurgeBarrier.HaringvlietBarrier.title}"

    questions = Database(database_path)
    questions.read()
    calendar = KnowledgeCalendar(
        output_dir=output_dir,
        output_file=output_file,
        questions=questions,
        storm_surge_barrier=StormSurgeBarrier.HaringvlietBarrier,
    )

    calendar.build()


def test_create_rp():
    rp_dir = base_dir + "/07 RP/01 Uitwerking"
    database_path = rp_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK RP.xlsx"
    output_dir = "C:/Test/"  # rp_dir
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda {StormSurgeBarrier.Ramspol.title}"

    questions = Database(database_path)
    questions.read()
    calendar = KnowledgeCalendar(
        output_dir=output_dir,
        output_file=output_file,
        questions=questions,
        storm_surge_barrier=StormSurgeBarrier.HaringvlietBarrier,
    )

    calendar.build()


def test_create_hijk():
    hijk_dir = base_dir + "/02 HIJK/01 Uitwerking"
    database_path = hijk_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK HIJK.xlsx"
    output_dir = "C:/Test/"  # rp_dir
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda {StormSurgeBarrier.HollandseIJsselBarrier.title}"

    questions = Database(database_path)
    questions.read()
    calendar = KnowledgeCalendar(
        output_dir=output_dir,
        output_file=output_file,
        questions=questions,
        storm_surge_barrier=StormSurgeBarrier.HaringvlietBarrier,
    )

    calendar.build()
