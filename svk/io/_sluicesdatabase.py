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

from svk.data import SluicesResearchQuestion, ResearchLine
from svk.io._exceldatabase import ExcelDatabase


class SluicesKnowledgeAgendaDatabase(ExcelDatabase, list[SluicesResearchQuestion]):
    """
    Class that wraps a list[ResearchQuestion] to allow additional logic to read an convert a database file stored in Excel.
    """

    # TODO: Change barrier icon to sluice icon and use that.
    i_sluice = "A"
    """A - Hard coded column number for the sluice"""
    i_id = "B"
    """B - Hard coded column number for the question id"""
    i_reference_ids = "C"
    """C - Hard coded column number for the references to other questions"""
    i_keywords = "D"
    """D - Hard coded column number for the keywords"""
    i_question = "E"
    """E - Hard coded column number for the question"""
    i_explanation = "F"
    """G - Hard coded column number for the question explanation"""
    i_prio_water_safety = "G"
    """H - Hard coded column number for the priority (water safety)"""
    i_prio_water_availability = "H"
    """I - Hard coded column number for the priority (water availability)"""
    i_prio_shipping = "I"
    """J - Hard coded column number for the priority (shipping function)"""
    i_prio_other_functions = "J"
    """K - Hard coded column number for the priority (functions other than water safety, shipping and water availability)"""
    i_prio_maintenance = "K"
    """L - Hard coded column number for the priority (management and maintenance)"""
    i_prio_operation = "L"
    """L - Hard coded column number for the prioties (operation)"""
    i_time_frame = "N"
    """N - Hard coded column number for the time frame"""
    i_research_line = "O"
    """O - Hard coded column number for the research line"""
    i_research_program = "P"
    """P - Hard coded column for the related research program"""
    i_status = "R"
    """R - Hard coded column number for the status"""
    i_contributes_to_standardisation = "Y"
    """Y - Hard coded column indicating whether the anwer contributes to standardisation"""

    def __init__(self, file_path: str):
        super().__init__(file_path, first_data_row=4)

    def read_and_append_row(self, row, i_row: int) -> None:
        self.append(
            SluicesResearchQuestion(
                id=ExcelDatabase._get_as_str(row, ExcelDatabase._string_to_column_index(self.i_id)),
                question=ExcelDatabase._get_as_str(row, ExcelDatabase._string_to_column_index(self.i_question)),
                explanation=ExcelDatabase._get_str_optional(row, ExcelDatabase._string_to_column_index(self.i_explanation)),
                sluice=ExcelDatabase._get_as_str(row, ExcelDatabase._string_to_column_index(self.i_sluice)),  # TODO: Change to sluices
                research_line=SluicesKnowledgeAgendaDatabase._get_research_line_optional(
                    row, ExcelDatabase._string_to_column_index(self.i_research_line)
                ),
                time_frame=ExcelDatabase._get_time_frame(row, ExcelDatabase._string_to_column_index(self.i_time_frame)),
                prio_management_maintenance=ExcelDatabase._get_priority(
                    row, ExcelDatabase._string_to_column_index(self.i_prio_maintenance)
                ),
                prio_shipping=ExcelDatabase._get_priority(row, ExcelDatabase._string_to_column_index(self.i_prio_shipping)),
                prio_other_functions=ExcelDatabase._get_priority(row, ExcelDatabase._string_to_column_index(self.i_prio_other_functions)),
                prio_operation=ExcelDatabase._get_priority(row, ExcelDatabase._string_to_column_index(self.i_prio_operation)),
                prio_water_safety=ExcelDatabase._get_priority(row, ExcelDatabase._string_to_column_index(self.i_prio_water_safety)),
                prio_water_availability=ExcelDatabase._get_priority(
                    row, ExcelDatabase._string_to_column_index(self.i_prio_water_availability)
                ),
                reference_ids=(
                    [
                        entry.strip()
                        for entry in ExcelDatabase._get_as_str(row, ExcelDatabase._string_to_column_index(self.i_reference_ids))
                        .replace(";", ",")
                        .split(",")
                        if entry.strip()
                    ]
                    if not ExcelDatabase._empty(row, ExcelDatabase._string_to_column_index(self.i_reference_ids))
                    else []
                ),
                keywords=ExcelDatabase._get_str_optional(row=row, i_column=ExcelDatabase._string_to_column_index(self.i_keywords)),
                contributes_to_standardisation=self._get_bool_from_str(
                    row, ExcelDatabase._string_to_column_index(self.i_contributes_to_standardisation)
                ),
            )
        )

    @staticmethod
    def _get_bool_from_str(row: tuple, i_column: int) -> bool:
        value = ExcelDatabase._get_as_str(row, i_column)
        return value.lower() in ("true", "1", "yes", "y", "ja", "nee")

    @staticmethod
    def _get_research_line_optional(row: tuple, i_column: int) -> ResearchLine | None:
        return None  # TODO: Implement all research lines of sluices and create own factory.
