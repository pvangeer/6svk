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

from svk.io import KnowledgeAgendaDatabase
import sys
import pytest

print(sys.path)


def test_database_creation_full_database_ssb_delta():
    d = KnowledgeAgendaDatabase("C:/src/6svk/test/test-data/example-SSB-delta.xlsx")
    d.read()
    if len(d) < 20:
        print("length = " + str(len(d)))
        for e in d.errors:
            print(e)
        pytest.fail("Database not read correctly")
