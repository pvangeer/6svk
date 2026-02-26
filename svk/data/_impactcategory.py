from enum import Enum


class ImpactCategory(Enum):
    SocioEconomicAndEnvironment = (
        1,
        "SSBs contribute to satisfying socio-economic and environmental needs in the hinterland",
        "The storm surge barriers contribute to satisfying the socio-economic and environmental needs in the hinterland. This implies that people, knowledge, data, and tools are available to determine what thehinterland requires from the storm surge barrier. These requirements will likely evolve over time due to changes in sea-level as well as changes in society.",
    )
    ReliableSSB = (
        2,
        "Reliable SSBs in technically good condition",
        "The storm surge barrier is reliable and in a good technical condition. The barrier is properly monitored and methods are available to determine the technical condition. Methods like an adaptive maintenance planning and people are available for timely decisions on maintenance and reinforcement of (parts of) the storm surge barrier in relation to the needs from the hinterland.",
    )
    MaintenanceDecisions = (
        3,
        "Well-balanced maintenance and end-of-life decisions for the SSBs by including the system, technical and economical perspective.",
        "A well-balanced maintenance is enabled and end-of-lifetime decision for the storm surge barriers can be made by including the system, technical and economical perspective. A time-based adaptive pathway is available to determine when a storm surge barrier reaches its end of life (functional and structural) and what the options and impacts are for maintenance, removal, replacement, closure. Supporting near-future decision making and avoiding maladaptation.",
    )
    HumanCapical = (
        4,
        "Human capital for a safe and liveable delta",
        "Human capital for a safe and liveable delta. There is a knowledgeable community of professionals that is enabled to cope with the challenges in deltas.",
    )
    Example = (
        5,
        "The Dutch Delta is an example how to deal with climate change in low-lying delta countries and the Dutch water sector remains a frontrunner",
        "The Dutch Delta is an example how to deal with climate change in low-lying delta-countries and the Dutch Water sector remains a frontrunner. Knowledge and experience are shared in an inclusive international community with organizations and countries facing similar climate challenges.",
    )

    def __init__(self, number: int, title: str, description: str):
        self.number = number
        self.title = title
        self.description = description
