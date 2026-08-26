from enum import Enum
from pydantic import BaseModel


class Label(Enum):
    TFNotRelevant = ("Niet relevant", "Not relevant")
    TFNow = ("Nu", "Now")
    TFNearFuture = ("Nabije toekomst", "Near future")
    TFFuture = ("Toekomst", "Future")
    TFUnknown = ("Onbekend", "Unknown")

    D_NoResearchLine = ("Zonder onderzoekslijn", "No research line")

    RL_ConstructiveAspects = ("Constructieve aspecten", "Structural aspects")
    RL_OperatingSystem = ("Besturingssystemen / IA", "Control systems / Industrial automation")
    RL_Facilities = ("Voorzieningen en gebouwen", "Facilities and buildings")
    RL_Maintenance = ("Onderhoud en operatie", "Maintenance and operation")
    RL_Cyber = ("Cyber & security", "Cyber & security")
    RL_Hydrodynamics = ("Hydrodynamische effecten en belastingen", "Hydrodynamic effects and loads")
    RL_ProbabilityOfFailyre = ("Faalkans", "Failure probability")
    RL_Adaptation = ("Adaptatie stormvloedkeringen", "System-level adaptation")
    RL_Organizational = ("Organisatorische aspecten", "Organisational aspects")
    RL_Lifespan = ("Restlevensduur huidige objecten", "Remaining lifetime")

    RL_TechnicalLifeTimeCivilParts = ("Technische levensduur civiele delen", "Technische levensduur - civiele delen")
    RL_TechnicalLifeTimeInstallations = ("Technische levensduur installaties", "Technische levensduur - installaties")
    RL_InspectionsMonitoringAndData = ("Inspecties, monitoring en data", "Inspecties, monitoring en data")
    RL_WaterSafety = ("Hoogwaterveiligheid", "Hoogwaterveiligheid")
    RL_WaterSystemAndAvailability = ("Watersysteem en waterbeschikbaarheid", "Watersysteem en waterbeschikbaarheid")
    RL_EcologyAndWaterQuality = ("Ecologie en waterkwaliteit watersysteem", "Ecologie en waterkwaliteit watersysteem")
    RL_Functions = (
        "Functies van het complex (scheepvaart, weg en water)",
        "Functies van het complex in het netwerk (scheepvaart, weg en water)",
    )
    RL_Operation = ("Operatie: bediening en besturing", "Operatie: bediening en besturing")
    RL_Robuustness = ("Beschikbaarheid en robuustheid", "Beschikbaarheid en robuustheid")
    RL_Strategy = ("Stategie, afweging en keuzes", "Stategie, afweging en keuzes")
    RL_EnvironmentalImpact = ("Milieu impact", "Milieu-impact")
    RL_SP_Organizational = ("Organisatorische aspecten", "Organisatorische aspecten")

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
    SSB_SluicePanheel = ("Sluis Panheel", "Panheel Sluices")

    QD_Related = ("Gerelateerd", "Related")
    QD_Drivers = ("Drivers", "Drivers")
    QD_Components = ("Componenten", "Components")
    QD_Functions = ("Functies", "Functions")
    QD_Priority = ("Prioriteit", "Priority")
    QD_Organizational = ("Organisatorisch", "Organizational")
    QD_CurrentResearch = ("Lopend onderzoek", "Current research")
    QD_WaterSafety = ("Waterveiligheid", "Water safety")
    QD_WaterAvailability = ("Waterbeschikbaarheid", "Water availability")
    QD_Shipping = ("Scheepvaart", "Shipping")
    QD_OtherFunctions = ("Ander functies", "Other functions")
    QD_Operation = ("Operatie", "Operation")
    QD_Maitenance = ("B&O", "Maintenance")
    QD_ResearchLineOne = ("Onderzoekslijn 1", "Research line 1")
    QD_ResearchLineTwo = ("Onderzoekslijn 2", "Research line 2")
    QD_ActionHolder = ("Belegd bij", "Action holder")
    QD_Status = ("Status", "Status")
    QD_Keywords = ("Trefwoorden", "Keywords")
    QD_Related_Questions = ("Gerelateerde vragen", "Related questions")
    QD_RelatedResearch = ("Gerelateerd onderzoek", "Related research")
    QD_AdressedInResearchProject = ("Belegd in programma", "Adressed in research project")

    def __init__(self, nl_label: str, en_label: str):
        self.nl = nl_label
        self.en = en_label


class Translator(BaseModel):
    lang: str = "nl"
    """supported values: nl (for Dutch) and en (for English)"""

    def get_label(self, label: Label) -> str:
        return label.en if self.lang == "en" else label.nl
