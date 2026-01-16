from svgwrite import Drawing
from svk.data import TimeFrame
from svk.visualization._header import Header
from svk.visualization._group import Group
from svk.visualization._timeframeaware import TimeFrameAware


class Column(TimeFrameAware):
    time_frame: TimeFrame
    groups: list[Group] = []
    column_width: int = 650
    group_margin: int = 20

    @property
    def header(self) -> Header:
        return Header(time_frame=self.time_frame)

    def get_width(self):
        return self.column_width

    def get_height(self):
        return self.header.height + sum([group.get_height() + self.group_margin for group in self.groups])

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

    def draw(self, dwg: Drawing, x: int, y: int):
        self.header.draw(dwg, x, y)

        current_y = y + self.header.height + self.group_margin
        for group in self.groups:
            group.arrow_depth = self.header.arrow_depth
            group.draw(dwg, x, current_y, round(self.column_width - self.header.arrow_depth))
            current_y += group.get_height() + self.group_margin
