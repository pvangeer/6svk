from pydantic import BaseModel
from svk.data import TimeFrame


class TimeFrameAware(BaseModel):
    time_frame: TimeFrame

    def grey_fraction(self) -> float:
        match self.time_frame:
            case TimeFrame.Now:
                return 0
            case TimeFrame.NearFuture:
                return 0.5
            case TimeFrame.Future:
                return 0.8
            case TimeFrame.NotRelevant:
                return 1
            case TimeFrame.Unknown:
                return 0.0
            case _:
                raise ValueError("Unknown time frame")
