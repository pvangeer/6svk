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

from svk.data import Translator
from svk.visualization import KnowledgeCalendarDocument
from svk.data import StormSurgeBarrier, Translator

from test.utils.database_reader import read_knowledge_agenda_database, get_database_dir, read_ssb_pathway_database
from test.paths import test_output_dir


def get_knowledge_calendar_output_file(barrier: StormSurgeBarrier, add: str | None = None) -> str:
    t = Translator(lang="nl")
    name = f"{datetime.now().strftime("%Y-%m-%d")} - Kennisagenda {t.get_label(barrier.title)}"
    if add is not None and add != "":
        name += f" - {add}"
    return name


@pytest.mark.product
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
def test_create_knowledge_calendar_per_ssb(barrier: StormSurgeBarrier):
    calendar_document = KnowledgeCalendarDocument(
        output_dir=get_database_dir(barrier=barrier),
        output_file=get_knowledge_calendar_output_file(barrier=barrier),
        questions=read_knowledge_agenda_database(barrier=barrier),
        storm_surge_barrier=barrier,
    )
    calendar_document.build()


@pytest.mark.product
def test_create_6svk():
    all_questions = (
        read_knowledge_agenda_database(StormSurgeBarrier.HartelBarrier)
        + read_knowledge_agenda_database(StormSurgeBarrier.HollandseIJsselBarrier)
        + read_knowledge_agenda_database(StormSurgeBarrier.HaringvlietBarrier)
        + read_knowledge_agenda_database(StormSurgeBarrier.MaeslantBarrier)
        + read_knowledge_agenda_database(StormSurgeBarrier.Ramspol)
        + read_knowledge_agenda_database(StormSurgeBarrier.EasternScheldtBarrier)
        + read_ssb_pathway_database()
    )
    six_svk_questions = tuple(q for q in all_questions if StormSurgeBarrier.All in q.storm_surge_barriers)
    calendar = KnowledgeCalendarDocument(
        output_dir=test_output_dir,
        output_file=get_knowledge_calendar_output_file(StormSurgeBarrier.All),
        questions=six_svk_questions,
        storm_surge_barrier=StormSurgeBarrier.All,
    )
    calendar.build()


@pytest.mark.product
def test_create_all():
    calendar = KnowledgeCalendarDocument(
        output_dir=test_output_dir,
        output_file=get_knowledge_calendar_output_file(StormSurgeBarrier.All, "alle vragen"),
        questions=read_knowledge_agenda_database(StormSurgeBarrier.HartelBarrier)
        + read_knowledge_agenda_database(StormSurgeBarrier.HollandseIJsselBarrier)
        + read_knowledge_agenda_database(StormSurgeBarrier.HaringvlietBarrier)
        + read_knowledge_agenda_database(StormSurgeBarrier.MaeslantBarrier)
        + read_knowledge_agenda_database(StormSurgeBarrier.Ramspol)
        + read_knowledge_agenda_database(StormSurgeBarrier.EasternScheldtBarrier)
        + read_ssb_pathway_database(),
        storm_surge_barrier=StormSurgeBarrier.All,
    )
    calendar.build()
