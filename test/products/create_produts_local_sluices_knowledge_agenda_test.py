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
from svk.data import SluicesResearchQuestion, TimeFrame, Translator
from svk.io import SluicesKnowledgeAgendaDatabase
from svk.visualization import SluicesDocument
from test.paths import test_data_dir, test_output_dir

import pytest


def read_database() -> list[SluicesResearchQuestion]:
    questions = SluicesKnowledgeAgendaDatabase(test_data_dir / "example_sp.xlsx")
    questions.read()

    if len(questions.errors) > 0:
        for e in questions.errors:
            print(e)
    return [q for q in questions if q.time_frame != TimeFrame.NotRelevant]


@pytest.mark.localproduct
def test_create_sluices_overview():
    questions = read_database()
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda Sluis Panheel"

    calendar = SluicesDocument(
        output_dir=test_output_dir,
        output_file=output_file,
        questions=questions,
    )

    calendar.build()
