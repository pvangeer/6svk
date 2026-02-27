from svk.data import (
    ImpactPathwayResearchQuestion,
    ImpactCategory,
)
from svk.io._exceldatabase import ExcelDatabase, DatabaseReadError


class ImpactPathwayDatabase(ExcelDatabase, list[ImpactPathwayResearchQuestion]):
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
    i_explanation = 7
    """Hard coded column number for the question explanation"""
    i_prio_water_safety = 8
    """Hard coded column number for the priority (water safety)"""
    i_prio_other_functions = 9
    """Hard coded column number for the priority (other functions)"""
    i_prio_management_maintenance = 10
    """Hard coded column number for the priority (management and maintenance)"""
    i_prio_operation = 11
    """Hard coded column number for the priority (operation)"""
    i_time_frame = 12
    """Hard coded column number for the time frame"""
    i_primary_research_line = 13
    """Hard coded column number for the primary research line"""
    i_secundary_research_line = 14
    """Hard coded column number for the secundary research line"""
    i_research_line_explanation = 17
    """Hard coded column number for the research line explanation"""
    i_status = 19
    """Hard coded column number for the status"""
    i_action_holder = 20
    """Hard coded column number for the action holder"""
    i_costs = 21
    """Hard coded column number for the costs"""
    i_lead_time = 22
    """Hard coded column number for the lead time"""
    i_impact_category = 16

    def read_and_append_row(self, row):
        self.append(
            ImpactPathwayResearchQuestion(
                id=ExcelDatabase._get_as_str(row, self.i_id),
                question=ExcelDatabase._get_as_str(row, self.i_question),
                impact_category=ImpactPathwayDatabase._get_impact_category(row, self.i_impact_category),
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
                keywords=ExcelDatabase._get_as_str(row=row, i_column=self.i_keywords),
            )
        )

    @staticmethod
    def _get_impact_category(row: tuple, i_column: int) -> ImpactCategory:
        category_string = ExcelDatabase._get_as_str(row, i_column)
        match category_string:
            case ImpactCategory.SocioEconomicAndEnvironment.title:
                return ImpactCategory.SocioEconomicAndEnvironment
            case ImpactCategory.ReliableSSB.title:
                return ImpactCategory.ReliableSSB
            case ImpactCategory.MaintenanceDecisions.title:
                return ImpactCategory.MaintenanceDecisions
            case ImpactCategory.HumanCapical.title:
                return ImpactCategory.HumanCapical
            case ImpactCategory.Example.title:
                return ImpactCategory.Example
            case _:
                raise DatabaseReadError("Cannot read impact category.", i_column=i_column)
