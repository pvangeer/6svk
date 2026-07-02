
from __future__ import annotations
from pydantic import model_validator, PrivateAttr
from svgwrite import Drawing
from svk.data import StormSurgeBarrier
from svk.visualization.elements._visual_elements_container import VisualElementsContainer
from svk.visualization.helpers._draw_scaled_icon import draw_scaled_icon

class SsbIconsElement(VisualElementsContainer):
    """A container for the storm surge barrier icons."""

    storm_surge_barriers: list[StormSurgeBarrier]
    """The storm surge barriers to display icons for."""

    _height: float = PrivateAttr()
    _width: float = PrivateAttr()

    @model_validator(mode="after")
    def validate(self) -> SsbIconsElement:
        
        self._width = (self.layout_configuration.small_margin + self.layout_configuration.icon_width_small) * len(self.storm_surge_barriers) + self.layout_configuration.small_margin
        self._height = (
            self.layout_configuration.small_margin
            + self.layout_configuration.icon_width_small
            + self.layout_configuration.small_margin
        )
        return self

    @property
    def height(self) -> float:
        return self._height

    @property
    def width(self) -> float:
        return self._width

    def draw(self, dwg: Drawing, x: float, y: float):
        x_icon_current = x + self.layout_configuration.small_margin
        y_icon_current = y + self.layout_configuration.small_margin
        for barrier in self.storm_surge_barriers:
            draw_scaled_icon(
                dwg=dwg,
                storm_surge_barrier=barrier,
                insert=(
                    x_icon_current,
                    y_icon_current,
                ),
                size=(self.layout_configuration.icon_width_small, self.layout_configuration.icon_width_small),
            )
            x_icon_current += self.layout_configuration.icon_width_small + self.layout_configuration.small_margin
