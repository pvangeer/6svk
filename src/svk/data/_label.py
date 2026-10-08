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

from enum import Enum


class Label(Enum):
    TFNotRelevant = ("Niet relevant", "Not relevant")
    TFNow = ("Nu", "Now")
    TFNearFuture = ("Nabije toekomst", "Near future")
    TFFuture = ("Toekomst", "Future")
    TFUnknown = ("Onbekend", "Unknown")

    LegendTitle = ("Legenda", "Legend")
    LegendHighPriority = ("Hoge prioriteit", "High priority")
    LegendLowPriority = ("Lage prioriteit", "Low priority")

    D_NoResearchLine = ("Zonder onderzoekslijn", "No research line")
    D_TitlePrefix = ("Details onderzoeksagenda", "Details research agenda")

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

    RLG_Maintenance = ("Onderhoudsvragen", "Maintenance questions")
    RLG_Requirements = ("Voldoen aan de eisen van vandaag en morgen", "Meeting today's requirements and tomorrow's challenges")
    RLG_Operational = ("Bedrijfskundige optimalisatie", "Operational optimization")

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
