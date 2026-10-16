from svk.data import Color, KnownColors
from svk.visualization.elements._visual_element import VisualElement


class GridCellElement(VisualElement):
    fill: Color = KnownColors.White
    i_row: int
    i_column: int

    def measure(self) -> None:
        self._width = self.layout_configuration.grid_cell_minimal_width
        self._height = self.layout_configuration.grid_cell_minimal_height

    def _draw(self, x: float, y: float):
        self._dwg.add(
            self._dwg.rect(
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
