from svgwrite import Drawing
from pydantic import model_validator, PrivateAttr

from svk.data import KnownColors
from svk.visualization.pages._page import Page
from svk.visualization.elements.panheel.legend._legend_element import LegendElement


class LegendPage(Page):
    _legend_element: LegendElement = PrivateAttr()
    title_link_target: str | None = "#legend_page"

    @model_validator(mode="after")
    def validate(self):
        self._legend_element = LegendElement(
            layout_configuration=self.layout_configuration,
            links_register=self.links_register,
            translator=self.translator,
            color=KnownColors.GreyAccent,
            use_contrast_color=True,
        )
        return self

    def get_content_size(self) -> tuple[float, float]:
        return (self._legend_element.width, self._legend_element.height)

    def draw_content(self, dwg: Drawing, left: float, top: float):
        self._legend_element.draw(dwg=dwg, x=left, y=top)
