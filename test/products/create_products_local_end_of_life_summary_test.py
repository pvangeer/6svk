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

from svk.data import StormSurgeBarrier
from svk.visualization import CustomPagesDocument, LifeTimeAnalysisPage

from test.utils.database_reader import read_end_of_life_database
from test.paths import test_output_dir


@pytest.mark.localproduct
def test_create_end_of_life_time_summary():
    pages = []
    page_count = 0
    document = CustomPagesDocument(
        output_dir=test_output_dir,
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
        efl = read_end_of_life_database(
            barrier=barrier,
            row_header_column=2 if barrier == StormSurgeBarrier.HaringvlietBarrier else 1,
            row_header_categories_column=1,
            sheet_name="EFL",
        )
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
                grid=efl,
            )
        )
        etl = read_end_of_life_database(
            barrier=barrier,
            row_header_column=1,
            row_header_categories_column=1,
            sheet_name="ETL",
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
                grid=etl,
            )
        )
        page_count += 1
    document.custom_pages = pages
    document.build()
