"""
Copyright (C) Stichting Deltares 2024. All rights reserved.

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

from svk.data import ResearchQuestion, Priority, ResearchLine, TimeFrame

from openpyxl import load_workbook
from pathlib import Path


class DatabaseReadError(Exception):
    def __init__(self, message: str, i_row: int | None = None, i_column: int | None = None):
        super().__init__(message)
        self.i_row = i_row
        self.i_column = i_column

    @property
    def cell_reference(self) -> str:
        reference = ""
        if self.i_column is not None:
            reference = self.__number_to_letter(self.i_column + 1)

        if self.i_row is not None:
            return reference + str(self.i_row + 1)

        return reference

    def __number_to_letter(self, n: int):
        return chr(ord("A") + n - 1)


class Database(list[ResearchQuestion]):
    i_barrier = 0
    i_id = 1
    i_reference_ids = 2
    i_reference_question = 3
    i_keywords = 4
    i_question = 5
    i_explanation = 6
    i_prio_water_safety = 7
    i_prio_other_functions = 8
    i_prio_management_maintenance = 9
    i_prio_operation = 10
    i_time_frame = 11
    i_primary_research_line = 12
    i_secundary_research_line = 13
    i_research_line_explanation = 14
    i_status = 15
    i_action_holder = 16
    i_costs = 17
    i_lead_time = 18

    def __init__(self, file_path: str):
        self.errors: list[DatabaseReadError] = []
        if not self._check_file_path(file_path):
            raise ValueError("Excel file could not be found.")

        self.file_path: str = file_path

    def _check_file_path(self, file_path: str) -> bool:
        p = Path(file_path)
        return p.exists() and p.is_file() and p.suffix.lower() in {".xls", ".xlsx", ".xlsm", ".xlsb"}

    def read(self, sheet_name: str = "Database", first_data_row: int = 3) -> bool:
        wb = load_workbook(self.file_path)
        sheet = wb[sheet_name]

        for i_row, row in enumerate(sheet.iter_rows(min_row=first_data_row, max_row=None, values_only=True)):
            try:
                self.append(
                    ResearchQuestion(
                        id=Database._get_str(row, self.i_id),
                        question=Database._get_str(row, self.i_question),
                        explanation=Database._get_str_optional(row, self.i_explanation),
                        storm_surge_barrier=Database._get_str(row, self.i_barrier).split(","),
                        research_line_primary=Database._get_research_line_optional(row, self.i_primary_research_line),
                        research_line_secondary=Database._get_research_line_optional(row, self.i_secundary_research_line),
                        time_frame=Database._get_time_frame(row, self.i_time_frame),
                        prio_management_maintenance=Database._get_priority(row, self.i_prio_management_maintenance),
                        prio_other_functions=Database._get_priority(row, self.i_prio_other_functions),
                        prio_operation=Database._get_priority(row, self.i_prio_operation),
                        prio_water_safety=Database._get_priority(row, self.i_prio_water_safety),
                        action_holder=Database._get_str_optional(row, self.i_action_holder),
                        lead_time=Database._get_int_optional(row, self.i_lead_time),
                        costs_estimate=Database._get_int_optional(row, self.i_costs),
                        reference_ids=(
                            Database._get_str(row, self.i_reference_ids).replace(";", ",").split(",")
                            if not Database._empty(row, self.i_reference_ids)
                            else []
                        ),
                        reference_question=Database._get_int_optional(row, self.i_reference_question),
                    )
                )
            except DatabaseReadError as e:
                e.i_row = i_row + first_data_row - 1
                self.errors.append(e)
                continue
        return True

    @staticmethod
    def _get_str(row: tuple, i_column: int) -> str:
        value = row[i_column]
        if not isinstance(value, str):
            raise DatabaseReadError("Read cell is of incorrect type.", i_column=i_column)

        return str(value)

    @staticmethod
    def _get_str_optional(row: tuple, i_column: int) -> str | None:
        value = row[i_column]
        if not isinstance(value, str) or value == "":
            return None

        return str(value)

    @staticmethod
    def _get_int(row: tuple, i_column: int) -> int:
        value = row[i_column]
        if not isinstance(value, int):
            raise DatabaseReadError("Read cell is of incorrect type.", i_column=i_column)

        return int(value)

    @staticmethod
    def _get_int_optional(row: tuple, i_column: int) -> int | None:
        value = row[i_column]
        if not isinstance(value, int) or value is None:
            return None

        return int(value)

    @staticmethod
    def _get_research_line_optional(row: tuple, i_column: int) -> ResearchLine | None:
        value = row[i_column]
        if not isinstance(value, str) or value is None:
            return None

        return ResearchLine.get_research_line(int(str(value).split(".")[0]))

    @staticmethod
    def _empty(row: tuple, i_column: int) -> bool:
        value = row[i_column]
        return value == None

    @staticmethod
    def _get_priority(row: tuple, i_column: int) -> Priority:
        value = row[i_column]
        if not isinstance(value, int):
            return Priority.Unknown

        match int(value):
            case 1:
                return Priority.Low
            case 2:
                return Priority.Medium
            case 3:
                return Priority.High
            case _:
                return Priority.Unknown

    @staticmethod
    def _get_time_frame(row: tuple, i_column: int) -> TimeFrame:
        value = row[i_column]
        if not isinstance(value, int):
            return TimeFrame.Unknown

        match int(value):
            case 0:
                return TimeFrame.NotRelevant
            case 1:
                return TimeFrame.Now
            case 2:
                return TimeFrame.NearFuture
            case 3:
                return TimeFrame.Future
            case _:
                return TimeFrame.Unknown
