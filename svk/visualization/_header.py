from svgwrite import Drawing
from pydantic import BaseModel
from svk.data import TimeFrame
from svk.visualization.helpers._greyfraction import color_toward_grey
from svk.visualization.helpers._drawchevron import chevron


class Header(BaseModel):
    time_frame: TimeFrame
    height: int = 80
    width: int = 650
    arrow_depth: int = 20
    text_margin: int = 10
    font_size: int = 18
    color: tuple[int, int, int] = (18, 103, 221)

    @property
    def title(self) -> str:
        match self.time_frame:
            case TimeFrame.Now:
                return "Nu"
            case TimeFrame.NearFuture:
                return "Boeggolf"
            case TimeFrame.Future:
                return "Toekomst"
            case TimeFrame.NotRelevant:
                return "Niet relevant"
            case TimeFrame.Unknown:
                return "Onbekend"
            case _:
                raise ValueError("Unknown time frame")

    @property
    def sub_title(self) -> str:
        match self.time_frame:
            case TimeFrame.Now:
                return ""
            case TimeFrame.NearFuture:
                return "(2033 - 2040))"
            case TimeFrame.Future:
                return "(>2040)"
            case TimeFrame.NotRelevant:
                return "(-)"
            case TimeFrame.Unknown:
                return "(?)"
            case _:
                raise ValueError("Unknown time frame")

    def draw(self, dwg: Drawing, x: int, y: int):
        draw_color = color_toward_grey(self.color, grey_fraction=self.time_frame.grey_fraction)
        dwg.add(chevron(dwg, x=x, y=y, width=self.width, height=self.height, id=self.title, color=draw_color))
        y_column_header_text = y + self.height / 2 + self.font_size / 2
        dwg.add(
            dwg.text(
                self.title,
                insert=(x + self.arrow_depth + self.text_margin, y_column_header_text),
                font_size=self.font_size,
                font_family="Arial",
                font_weight="bold",
                text_anchor="start",
                dominant_baseline="middle",
            )
        )
        if self.sub_title != "":
            dwg.add(
                dwg.text(
                    self.sub_title,
                    insert=(x + self.width - self.arrow_depth, y_column_header_text),
                    font_family="Arial",
                    text_anchor="end",
                    dominant_baseline="middle",
                    font_size=self.font_size,
                    font_weight="normal",
                )
            )
