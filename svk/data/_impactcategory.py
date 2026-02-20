from enum import Enum


class ImpactCategory(Enum):
    SocioEconomicAndEnvironment = (1, "SSBs contribute to satisfying socio-economic and environmental needs in the hinterland")
    ReliableSSB = (2, "Reliable SSBs in technically good condition")
    MaintenanceDecisions = (
        3,
        "Well-balanced maintenance and end-of-life decisions for the SSBs by including the system, technical and economical perspective.",
    )
    HumanCapical = (4, "Human capital for a safe and liveable delta")
    Example = (
        5,
        "The Dutch Delta is an example how to deal with climate change in low-lying delta countries and the Dutch water sector remains a frontrunner",
    )

    def __init__(self, number: int, description: str):
        self.number = number
        self.description = description
