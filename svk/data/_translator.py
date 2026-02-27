from enum import Enum
from pydantic import BaseModel


class Label(Enum):
    TFNotRelevant = ("Niet relevant", "Not relevant")
    TFNow = ("Nu", "Now")
    TFNearFuture = ("Nabije toekomst", "Near future")
    TFFuture = ("Toekomst", "Future")
    TFUnknown = ("Onbekend", "Unknown")

    # TODO: Check translation
    RL_ConstructiveAspects = ("Constructieve aspecten", "Structural aspects")
    RL_OperatingSystem = ("Besturingssystemen / IA", "Operating system / IA")
    RL_Facilities = ("Voorzieningen en gebouwen", "Facilities and buildings")
    RL_Maintenance = ("Onderhoud en operatie", "Maintenance")
    RL_Cyber = ("Cyber & security", "Cyber & security")
    RL_Hydrodynamics = ("Hydrodynamische effecten en belastingen", "Hydrodynamic effects and loads")
    RL_ProbabilityOfFailyre = ("Faalkans", "Probability of failure")
    RL_Adaptation = ("Adaptatie stormvloedkeringen", "Adaptation storm surge barriers")
    RL_Organizational = ("Organisatorische aspecten", "Organizational aspects")
    RL_Lifespan = ("Restlevensduur huidige objecten", "Remaining lifetime current objects")

    P_High = ("hoog", "high")
    P_Medium = ("middel", "medium")
    P_Low = ("laag", "low")
    P_No = ("geen", "no")
    P_Unknown = ("onbekend", "unknown")

    SSB_All = ("6SVK", "6SSB")
    SSB_MaeslantBarrier = ("Maeslantkering", "Maeslant Storm Barrier")
    SSB_HartelBarrier = ("Hartelkering", "Hartel Barrier")
    SSB_Ramspol = ("Ramspol", "Ramspol")
    SSB_HollandseIJsselBarrier = ("Hollandsche IJssel Kering", "Hollandsche IJssel Barrier")
    SSB_EasternScheldBarrier = ("Oosterscheldekering", "Eastern Scheldt Barrier")
    SSB_HaringvlietBarrier = ("Haringvlietsluizen", "Haringvliet Sluices")

    QD_Related = ("Gerelateerd", "Related")
    QD_Priority = ("Prioriteit", "Priority")
    QD_WaterSafety = ("Waterveiligheid", "Water safety")
    QD_OtherFunctions = ("Ander functies", "Other functions")
    QD_Operation = ("Operatie", "Operation")
    QD_Maitenance = ("B&O", "Maintenance")

    def __init__(self, nl_label: str, en_label: str):
        self.nl = nl_label
        self.en = en_label


class Translator(BaseModel):
    lang: str = "nl"
    """supported values: nl (for Dutch) and en (for English)"""

    def get_label(self, label: Label) -> str:
        return label.en if self.lang == "en" else label.nl
