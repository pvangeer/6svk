from __future__ import annotations
from pydantic import model_validator, PrivateAttr
from svgwrite import Drawing
from svk.data import TimeFrame
from svk.visualization.elements._visual_elements_container import VisualElementsContainer
from svk.visualization.helpers._draw_scaled_icon import Symbol, Path, accent_fill


class TimeFrameElement(VisualElementsContainer):
    """A container for the storm surge barrier icons."""

    time_frame: TimeFrame
    """The storm surge barriers to display icons for."""

    _height: float = PrivateAttr()
    _width: float = PrivateAttr()

    @model_validator(mode="after")
    def validate(self) -> TimeFrameElement:

        self._width = (
            self.layout_configuration.small_margin + self.layout_configuration.icon_width_small + self.layout_configuration.small_margin
        )
        self._height = (
            self.layout_configuration.small_margin + self.layout_configuration.icon_width_small + self.layout_configuration.small_margin
        )
        return self

    @property
    def height(self) -> float:
        return self._height

    @property
    def width(self) -> float:
        return self._width

    def draw(self, dwg: Drawing, x: float, y: float):
        time_frame_ico = Symbol(id=self.time_frame.name)

        match self.time_frame:
            case TimeFrame.Now:
                time_frame_ico.objects = [
                    Path(
                        d="m 52.550102,189.38019 153.669208,-0.19083 0.1952,72.93908 m 47.44872,-40.78067 -46.99687,40.47311 m -45.43164,-40.73769 44.67828,41.15982"
                    ),
                ]
            case TimeFrame.NearFuture:
                time_frame_ico.objects = [
                    Path(
                        d="m 58.082886,173.69718 179.530904,0.30091 m -40.78067,-47.44872 40.47311,46.99687 m -40.73769,45.43164 41.15982,-44.67828"
                    ),
                ]
            case TimeFrame.Future:
                time_frame_ico.objects = [
                    Path(
                        d="M 34.048204,170.95036 C 95.440663,82.251406 178.95804,105.79218 237.61379,173.99809 m 0.42164,-42.29843 -0.7292,41.84658 m -44.17122,0.45245 44.59335,0.30091"
                    ),
                    Path(d="M 59.743352,173.04971 H 76.910983", stroke_width=10, fill=accent_fill),
                    Path(d="M 92.682122,172.58829 H 109.84975", stroke_width=10, fill=accent_fill),
                    Path(d="M 125.09055,172.95992 H 17.16763", stroke_width=10, fill=accent_fill),
                    Path(d="M 158.21396,173.14573 H 17.16763", stroke_width=10, fill=accent_fill),
                ]

        x_icon_current = x + self.layout_configuration.small_margin
        y_icon_current = y + self.layout_configuration.small_margin

        time_frame_ico.add_to_dwg(
            dwg=dwg,
            insert=(
                x_icon_current,
                y_icon_current,
            ),
            size=(self.layout_configuration.icon_width_small, self.layout_configuration.icon_width_small),
        )
