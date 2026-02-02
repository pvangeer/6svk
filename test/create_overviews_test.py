"""
Copyright (C) Stichting Deltares 2026. All rights reserved.

This file is part of the dikernel-python toolbox.

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

from svk.io import Database
from svk.visualization import create_image_from_database
from svk.data import StormSurgeBarrier
from datetime import datetime

base_dir = "C:/Users/geer/OneDrive - Stichting Deltares/Projecten/Kennisvragen SVK"


def convert_database(database_path, storm_surge_barrier: StormSurgeBarrier, output_dir: str):
    now = datetime.now().strftime("%Y-%m-%d")

    print(f"Read questions from database: {database_path }")
    questions = Database(database_path)
    questions.read()

    for e in questions.errors:
        print(f"{e.cell_reference}: {str(e)}")

    # target_file_path = f"{output_dir}/{now} - Kennisvragen {storm_surge_barrier.title}.pdf"
    target_file_path = f"c:/Test/{now} - Kennisvragen {storm_surge_barrier.title}.pdf"
    print(f"create image: {target_file_path}")
    create_image_from_database(
        storm_surge_barrier.title,
        questions,
        target_file_path,
        barrier_icon=storm_surge_barrier,
    )


def test_create_overview_hv():
    hv_dir = base_dir + "/03 HV/01 Uitwerking"
    convert_database(
        database_path=hv_dir + "/Eerste toepassing methodiek kennisvragen SVK HV_Concept.xlsx",
        storm_surge_barrier=StormSurgeBarrier.HaringvlietBarrier,
        output_dir=hv_dir,
    )


def test_create_overview_rp():
    rp_dir = base_dir + "/07 RP/01 Uitwerking"
    convert_database(
        database_path=rp_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK RP.xlsx",
        storm_surge_barrier=StormSurgeBarrier.Ramspol,
        output_dir=rp_dir,
    )


def test_create_overview_hijk():
    hijk_dir = base_dir + "/02 HIJK/01 Uitwerking"
    convert_database(
        database_path=hijk_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK HIJK.xlsx",
        storm_surge_barrier=StormSurgeBarrier.HollandseIJsselBarrier,
        output_dir=hijk_dir,
    )
