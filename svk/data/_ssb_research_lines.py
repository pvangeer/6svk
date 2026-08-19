from enum import Enum
from svk.data._translator import Label


class StormSurgeBarrierResearchLines(Enum):
    """
    This enum exposes default research line objects used in the SVK-project.
    """

    ConstructiveAspects = (1, Label.RL_ConstructiveAspects, 1)
    OperatingSystem = (2, Label.RL_OperatingSystem, 1)
    Facilities = (3, Label.RL_Facilities, 1)
    Maintenance = (4, Label.RL_Maintenance, 1)
    Cyber = (5, Label.RL_Cyber, 2)
    Hydrodynamics = (6, Label.RL_Hydrodynamics, 2)
    ProbabilityOfFailyre = (7, Label.RL_ProbabilityOfFailyre, 2)
    Adaptation = (8, Label.RL_Adaptation, 2)
    Organizational = (9, Label.RL_Organizational, 3)
    Lifespan = (10, Label.RL_Lifespan, 3)

    def __init__(self, number: int, title: Label, cluster: int):
        self.id: str = "#RL-" + str(number)
        self.number: int = number
        self.title: Label = title
        self.cluster: int = cluster
