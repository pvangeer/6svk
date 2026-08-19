from svk.data._ssb_research_question import StormSurgeBarrierResearchQuestion
from svk.data._impactcategory import ImpactCategory
from svk.data._priority import Priority


class ImpactPathwayResearchQuestion(StormSurgeBarrierResearchQuestion):
    impact_category: ImpactCategory
    prio_urgency_decision_making: Priority

    @property
    def priority(self) -> int:
        prios = [
            self.prio_management_maintenance,
            self.prio_operation,
            self.prio_other_functions,
            self.prio_urgency_decision_making,
            self.prio_water_safety,
        ]
        combined_priority = sum([p.id for p in prios])
        n_high_prio = sum(1 for p in prios if p.id == 3)
        if n_high_prio > 1 or combined_priority > 10:
            return 2
        if n_high_prio > 0 or combined_priority > 8:
            return 1
        return 0
