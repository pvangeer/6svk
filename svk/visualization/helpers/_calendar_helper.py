from svk.data import ResearchQuestion, TimeFrame
from svk.visualization.helpers._greyfraction import color_toward_grey


def get_priority(question: ResearchQuestion) -> int:
    return 1 if question.has_priority else 0


def get_subtitle(time_frame: TimeFrame) -> str:
    match time_frame:
        case TimeFrame.Now:
            return ""
        case TimeFrame.NearFuture:
            return "(2033 - 2040)"
        case TimeFrame.Future:
            return "(>2040)"
        case TimeFrame.NotRelevant:
            return "(-)"
        case TimeFrame.Unknown:
            return "(?)"
        case _:
            raise ValueError("Unknown time frame")


def get_header_color(time_frame: TimeFrame) -> str:
    return color_toward_grey((18, 103, 221), grey_fraction=time_frame.grey_fraction)
