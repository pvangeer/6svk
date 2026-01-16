from pydantic import BaseModel

from svk.data import TimeFrame
from svk.visualization._column import Column

from svgwrite import Drawing


class Figure(BaseModel):
    columns: list[Column] = [Column(time_frame=TimeFrame.Now), Column(time_frame=TimeFrame.NearFuture), Column(time_frame=TimeFrame.Future)]
    paper_margin: int = 20

    def draw(self) -> Drawing:
        column_widths = [column.get_width() for column in self.columns]
        column_heights = [column.get_height() for column in self.columns]

        dwg = Drawing(size=(f"{self.paper_margin * 2 + sum(column_widths)}px", f"{self.paper_margin * 2 + max(column_heights)}px"))

        x_current = self.paper_margin
        for column in self.columns:
            column.draw(dwg, x_current, self.paper_margin)
            x_current = x_current + column.get_width()

        return dwg
