from enum import Enum
from svk.data._translator import Label


class SluicesResearchLines(Enum):
    """
    This enum exposes default research line objects used in the Panheel sluice-project.
    """

    TechnicalLifeTimeCivilParts = (1, Label.RL_TechnicalLifeTimeCivilParts, 1)
    TechnicalLifeTimeInstallations = (2, Label.RL_TechnicalLifeTimeInstallations, 1)
    InspectionsMonitoringAndData = (3, Label.RL_InspectionsMonitoringAndData, 1)
    WaterSafety = (4, Label.RL_WaterSafety, 2)
    WaterSystemAndAvailability = (5, Label.RL_WaterSystemAndAvailability, 2)
    EcologyAndWaterQuality = (6, Label.RL_EcologyAndWaterQuality, 2)
    Functions = (7, Label.RL_Functions, 2)
    Operation = (8, Label.RL_Operation, 2)
    Robustness = (9, Label.RL_Robuustness, 2)
    Strategy = (10, Label.RL_Strategy, 2)
    EnvironmentalImpact = (11, Label.RL_EnvironmentalImpact, 2)
    Organizational = (12, Label.RL_SP_Organizational, 3)

    def __init__(self, number: int, title: Label, cluster: int):
        self.id: str = "#RL-" + str(number)
        self.number: int = number
        self.title: Label = title
        self.cluster: int = cluster
