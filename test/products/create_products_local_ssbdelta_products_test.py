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
from svk.visualization import ImpactPathwayDocument
from test.paths import test_output_dir
from test.utils.database_reader import read_ssb_pathway_database


@pytest.mark.product
def test_create_impact_pathway():
    questions = read_ssb_pathway_database()
    output_file = f"{datetime.now().strftime("%Y-%m-%d")} - Impact pathway SSB-delta"

    pathway = ImpactPathwayDocument(questions=questions, output_dir=test_output_dir, output_file=output_file, cleanup=False)
    pathway.build()
