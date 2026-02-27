from pydantic import BaseModel
from svk.data import LinksRegister, Translator
from svk.visualization._layout_configuration import LayoutConfiguration
from svgwrite import Drawing


class VisualElement(BaseModel):
    layout_configuration: LayoutConfiguration
    """The layout configuration shared across all elements of a document."""
    links_register: LinksRegister
    translator: Translator

    def draw_vertical_separator(self, dwg: Drawing, x: float, y: float, element_height: float, color: str):
        dwg.add(
            dwg.line(
                start=(x, y + self.layout_configuration.small_margin),
                end=(x, y + element_height - self.layout_configuration.small_margin),
                stroke_width=0.5,
                stroke=color,
            )
        )

    def draw_horizontal_separator(self, dwg: Drawing, x: float, y: float, element_width: float, color: str):
        dwg.add(
            dwg.line(
                start=(x + self.layout_configuration.small_margin, y),
                end=(x + element_width - self.layout_configuration.small_margin, y),
                stroke_width=0.5,
                stroke=color,
            )
        )
