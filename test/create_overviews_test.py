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

from svk.io import Database, LinksManager
from svk.visualization import create_image_from_database, LayoutConfiguration, DetailsPage, QuestionDetails
from svk.data import StormSurgeBarrier
from svk.io import svg_to_pdf, merge_pdf_files, add_links
import os

base_dir = "C:/Users/geer/OneDrive - Stichting Deltares/Projecten/Kennisvragen SVK"


def convert_database_to_overview(
    config: LayoutConfiguration, links_manager: LinksManager, questions: Database, storm_surge_barrier: StormSurgeBarrier, output_dir: str
):
    now = datetime.now().strftime("%Y-%m-%d")

    for e in questions.errors:
        print(f"{e.cell_reference}: {str(e)}")

    output_dir = f"c:/Test/"
    file_name = f"{now} - Kennisvragen {storm_surge_barrier.title}"
    target_file_path = os.path.join(output_dir, file_name + ".pdf")
    print(f"create image: {target_file_path}")
    return create_image_from_database(
        config,
        links_manager,
        storm_surge_barrier.title,
        questions,
        output_dir,
        file_name,
        barrier_icon=storm_surge_barrier,
    )


def convert_database_to_details(
    config: LayoutConfiguration, links_manager: LinksManager, questions: Database, storm_surge_barrier: StormSurgeBarrier, output_dir: str
):
    dwg_details_page = DetailsPage(layout_configuration=config, links_manager=links_manager)
    for question in sorted(questions, key=lambda q: q.id):
        dwg_details_page.questions.append(
            QuestionDetails(layout_configuration=config, links_manager=links_manager, research_question=question)
        )

    now = datetime.now().strftime("%Y-%m-%d")
    # target_file_path = f"{output_dir}/{now} - Kennisvragen {storm_surge_barrier.title}.pdf"
    target_file_path = f"c:/Test/{now} - Kennisvragen {storm_surge_barrier.title} - details.pdf"
    output_dir = f"c:/Test/"
    file_name = f"{now} - Kennisvragen {storm_surge_barrier.title} - details"
    print(f"create image: {target_file_path}")

    return svg_to_pdf(dwg=dwg_details_page.draw(), output_dir=output_dir, file_name=file_name)


def test_create_overview_hv():
    hv_dir = base_dir + "/03 HV/01 Uitwerking"
    database_path = hv_dir + "/Eerste toepassing methodiek kennisvragen SVK HV_Concept.xlsx"

    config = LayoutConfiguration()
    links_manager = LinksManager()
    print(f"Read questions from database: {database_path }")
    questions = Database(database_path)
    questions.read()

    file_overview = convert_database_to_overview(
        config,
        links_manager,
        questions,
        storm_surge_barrier=StormSurgeBarrier.HaringvlietBarrier,
        output_dir=hv_dir,
    )

    file_details = convert_database_to_details(
        config=config,
        links_manager=links_manager,
        questions=questions,
        storm_surge_barrier=StormSurgeBarrier.HaringvlietBarrier,
        output_dir=hv_dir,
    )
    output_file = "C:/Test/Kennisvragen HV - all.pdf"
    final_output_file = "C:/Test/Kennisvragen HV - all with links.pdf"
    merge_pdf_files([file_overview, file_details], output_file)

    add_links(input_pdf_file=output_file, output_file=final_output_file, links_manager=links_manager)


def test_create_overview_rp():
    rp_dir = base_dir + "/07 RP/01 Uitwerking"
    database_path = rp_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK RP.xlsx"

    config = LayoutConfiguration()
    links_manager = LinksManager()

    print(f"Read questions from database: {database_path }")
    questions = Database(database_path)
    questions.read()

    convert_database_to_overview(
        config=config,
        links_manager=links_manager,
        questions=questions,
        storm_surge_barrier=StormSurgeBarrier.Ramspol,
        output_dir=rp_dir,
    )


def test_create_overview_hijk():
    hijk_dir = base_dir + "/02 HIJK/01 Uitwerking"
    database_path = hijk_dir + "/Concept Eerste toepassing methodiek kennisvragen SVK HIJK.xlsx"

    config = LayoutConfiguration()
    links_manager = LinksManager()

    print(f"Read questions from database: {database_path }")
    questions = Database(database_path)
    questions.read()

    convert_database_to_overview(
        config=config,
        links_manager=links_manager,
        questions=questions,
        storm_surge_barrier=StormSurgeBarrier.HollandseIJsselBarrier,
        output_dir=hijk_dir,
    )
