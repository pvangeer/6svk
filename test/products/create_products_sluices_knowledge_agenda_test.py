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
from svk.visualization import SluicesDocument
from test.paths import ph_base_dir
from test.utils.database_reader import read_ph_database

import pytest


# TODO: This duplicates code. Consider a shared logic function and call with different output_dir for local and product tests.
@pytest.mark.product
def test_create_sluices_overview():
    questions = read_ph_database()
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda Sluis Panheel"

    calendar = SluicesDocument(
        output_dir=ph_base_dir,
        output_file=output_file,
        questions=questions,
        cleanup=True,
    )

    calendar.build()
