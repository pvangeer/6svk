from svgwrite import Drawing
from pydantic import PrivateAttr, model_validator
from svk.data._color import Color, KnownColors
from svk.visualization.elements._visual_element import VisualElement


class GridCellElement(VisualElement):
    fill: Color = KnownColors.White
    i_row: int
    i_column: int
    _width: float = PrivateAttr()
    _height: float = PrivateAttr()

    @model_validator(mode="after")
    def validate(self):
        self._width = self.layout_configuration.grid_cell_minimal_width
        self._height = self.layout_configuration.grid_cell_minimal_height
        return self

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    def draw(self, dwg: Drawing, x: float, y: float):
        dwg.add(
            dwg.rect(
                insert=(x, y),
                size=(self.width, self.height),
                rx=10,  # horizontal corner radius TODO: move to layout_configuration
                ry=10,  # vertical corner radius
                fill=str(self.fill),
                fill_opacity=0.2 if self.fill == KnownColors.White else 0.7,
                stroke=str(self.fill),
                stroke_width=1,
            )
        )
