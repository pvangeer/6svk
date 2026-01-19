from svgwrite import Drawing
from svk.data import TimeFrame
from svk.visualization._header import Header
from svk.visualization._group import Group
from pydantic import BaseModel


class Column(BaseModel):
    time_frame: TimeFrame
    groups: list[Group] = []
    column_width: int = 650
    group_margin: int = 20
    y_group_1: int | None = None
    y_group_2: int | None = None
    y_group_3: int | None = None

    @property
    def header(self) -> Header:
        return Header(time_frame=self.time_frame)

    def get_width(self):
        return self.column_width

    def get_height(self):
        if self.y_group_3 is not None:
            return self.y_group_3 + sum(
                [group.get_height() + self.group_margin for group in self.groups if group.research_line.color_group == 3]
            )
        elif self.y_group_2 is not None:
            return self.y_group_2 + sum(
                [group.get_height() + self.group_margin for group in self.groups if group.research_line.color_group > 1]
            )
        else:
            return self.header.height + sum([group.get_height() + self.group_margin for group in self.groups])

    def grey_fraction(self) -> float:
        return self.time_frame.grey_fraction

    def draw(self, dwg: Drawing, x: int, y: int):
        self.header.draw(dwg, x, y)

        current_y = y + self.header.height + self.group_margin
        current_group_no = self.groups[0] if self.groups else 1
        for group in self.groups:
            if current_group_no != group.research_line.color_group:
                current_group_no = group.research_line.color_group
                y_new = (
                    self.y_group_1
                    if group.research_line.color_group == 1
                    else self.y_group_2 if group.research_line.color_group == 2 else self.y_group_3
                )
                if y_new is not None:
                    current_y = y_new

            group.arrow_depth = self.header.arrow_depth
            group.draw(dwg, x, current_y, round(self.column_width - self.header.arrow_depth))
            current_y += group.get_height() + self.group_margin
