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

from svk.data import StormSurgeBarrier, Translator
from svk.visualization import LifeTimeAnalysDocument

from test.utils.database_reader import read_end_of_life_database
from test.paths import test_output_dir


@pytest.mark.localproduct
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
@pytest.mark.localproduct
def test_create_end_of_life_analysis_document(barrier: StormSurgeBarrier):
    efl = read_end_of_life_database(
        barrier=barrier,
        row_header_column=2 if barrier == StormSurgeBarrier.HaringvlietBarrier else 1,
        row_header_categories_column=1,
        sheet_name="EFL",
    )
    etl = read_end_of_life_database(
        barrier=barrier,
        row_header_column=1,
        row_header_categories_column=1,
        sheet_name="ETL",
    )
    document = LifeTimeAnalysDocument(
        storm_surge_barrier=barrier,
        functional_lifetime_grid=efl,
        technical_lifetime_grid=etl,
        output_dir=test_output_dir,
        output_file=f"{datetime.now().strftime("%Y-%m-%d")} - Einde levensduur analyse {Translator(lang="nl").get_label(barrier.title)}",
    )
    document.build()
