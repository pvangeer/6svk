from svgwrite import Drawing
from pydantic import PrivateAttr, model_validator
from svk.io._endoflifedatabase import EndOfLifeCell, Color
from svk.visualization.elements._visual_element import VisualElement


class GridCellElement(VisualElement):
    fill: Color = Color.White
    i_row: int
    i_column: int
    _width: float = PrivateAttr()
    _height: float = PrivateAttr()

    @model_validator(mode="after")
    def validate(self):
        self._width = self.layout_configuration.grid_cell_min_width
        self._height = self.layout_configuration.grid_cell_min_height
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
                fill="#" + self.fill.value,
                stroke="#" + self.fill.value,
                stroke_width=0,
            )
        )
