from svgwrite import Drawing
from pydantic import model_validator

from svk.visualization.pages._page import Page
from svk.visualization.elements._grid_element import GridElement, Grid


class LifeTimeAnalysisPage(Page):
    grid: Grid

    @model_validator(mode="after")
    def validate(self):
        self._grid_element = GridElement(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            grid=self.grid,
        )

        return self

    def get_content_size(self) -> tuple[float, float]:
        return (self._grid_element.width, self._grid_element.height)

    def draw_content(self, dwg: Drawing, left: float, top: float):
        self._grid_element.draw(dwg=dwg, x=left, y=top)
