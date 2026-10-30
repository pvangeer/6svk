from svgwrite import Drawing
from pydantic import PrivateAttr

from svk.data import KnownColors
from svk.visualization.pages._page import Page
from svk.visualization.elements.legend._ssb_legend_element import StormSurgeBarrierLegendElement


class StormSurgeBarrierLegendPage(Page):
    _legend_element: StormSurgeBarrierLegendElement = PrivateAttr()
    title_link_target: str | None = "#legend_page"  # TODO: Put this in a general setting instead of hard coding this in different places.
    title: str = "Verklaring"
    subtitle: str = "Gebruikte symbolen, kleuren en vraagcodes"

    def initialize(self):
        super().initialize()
        self._legend_element = self.create(
            StormSurgeBarrierLegendElement,
            color=KnownColors.GreyAccent,
            use_contrast_color=True,
        )
        return self

    def get_content_size(self) -> tuple[float, float]:
        return (self._legend_element.width, self._legend_element.height)

    def draw_content(self, dwg: Drawing, left: float, top: float):
        self._legend_element.draw(dwg=dwg, x=left, y=top)
