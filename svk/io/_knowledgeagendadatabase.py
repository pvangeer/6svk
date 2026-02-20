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

from svk.data import ResearchQuestion
from svk.io._exceldatabase import ExcelDatabase


class KnowledgeAgendaDatabase(ExcelDatabase, list[ResearchQuestion]):
    """
    Class that wraps a list[ResearchQuestion] to allow additional logic to read an convert a database file stored in Excel.
    """

    i_barrier = 0
    """Hard coded column number for the barrier"""
    i_id = 1
    """Hard coded column number for the question id"""
    i_reference_ids = 2
    """Hard coded column number for the references to other questions"""
    i_reference_question = 3
    """Hard coded column number for the reference number to the 160 questions list"""
    i_keywords = 4
    """Hard coded column number for the keywords"""
    i_question = 5
    """Hard coded column number for the question"""
    i_explanation = 6
    """Hard coded column number for the question explanation"""
    i_prio_water_safety = 7
    """Hard coded column number for the priority (water safety)"""
    i_prio_other_functions = 8
    """Hard coded column number for the priority (other functions)"""
    i_prio_management_maintenance = 9
    """Hard coded column number for the priority (management and maintenance)"""
    i_prio_operation = 10
    """Hard coded column number for the priority (operation)"""
    i_time_frame = 11
    """Hard coded column number for the time frame"""
    i_primary_research_line = 12
    """Hard coded column number for the primary research line"""
    i_secundary_research_line = 13
    """Hard coded column number for the secundary research line"""
    i_research_line_explanation = 14
    """Hard coded column number for the research line explanation"""
    i_status = 15
    """Hard coded column number for the status"""
    i_action_holder = 16
    """Hard coded column number for the action holder"""
    i_costs = 17
    """Hard coded column number for the costs"""
    i_lead_time = 18
    """Hard coded column number for the lead time"""

    def read_and_append_row(self, row):
        self.append(
            ResearchQuestion(
                id=ExcelDatabase._get_as_str(row, self.i_id),
                question=ExcelDatabase._get_as_str(row, self.i_question),
                explanation=ExcelDatabase._get_str_optional(row, self.i_explanation),
                storm_surge_barriers=ExcelDatabase._get_storm_surge_barriers(row, self.i_barrier),
                research_line_primary=ExcelDatabase._get_research_line_optional(row, self.i_primary_research_line),
                research_line_secondary=ExcelDatabase._get_research_line_optional(row, self.i_secundary_research_line),
                time_frame=ExcelDatabase._get_time_frame(row, self.i_time_frame),
                prio_management_maintenance=ExcelDatabase._get_priority(row, self.i_prio_management_maintenance),
                prio_other_functions=ExcelDatabase._get_priority(row, self.i_prio_other_functions),
                prio_operation=ExcelDatabase._get_priority(row, self.i_prio_operation),
                prio_water_safety=ExcelDatabase._get_priority(row, self.i_prio_water_safety),
                action_holder=ExcelDatabase._get_str_optional(row, self.i_action_holder),
                lead_time=ExcelDatabase._get_int_optional(row, self.i_lead_time),
                costs_estimate=ExcelDatabase._get_int_optional(row, self.i_costs),
                reference_ids=(
                    [
                        entry.strip()
                        for entry in ExcelDatabase._get_as_str(row, self.i_reference_ids).replace(";", ",").split(",")
                        if entry.strip()
                    ]
                    if not ExcelDatabase._empty(row, self.i_reference_ids)
                    else []
                ),
                reference_question=ExcelDatabase._get_int_optional(row, self.i_reference_question),
            )
        )
