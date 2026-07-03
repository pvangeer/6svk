from svgwrite import Drawing
from pydantic import PrivateAttr, model_validator
from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.elements._visual_element import VisualElement
from svk.data import Label

class TitleElement(VisualElement):
    title: Label

    _height: float = PrivateAttr()
    _width: float = PrivateAttr()
    
    @model_validator(mode="after")
    def validate(self):
        self._width = (
            self.layout_configuration.small_margin
            + measure_text(self.translator.get_label(self.title), self.layout_configuration.font_size)[0]
            + self.layout_configuration.small_margin
            )
        self._height = (
            self.layout_configuration.small_margin 
            + self.layout_configuration.font_size * 1.2 
            + self.layout_configuration.small_margin
            )
        return self
    
    @property
    def height(self) -> float:
        return self._height

    @property
    def width(self) -> float:
        return self._width

    def draw(self, dwg: Drawing, x: float, y: float) -> None:
        dwg.add(
            dwg.text(
                self.translator.get_label(self.title),
                insert=(
                    x + self.layout_configuration.small_margin,
                    y + self.layout_configuration.small_margin
                ),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                font_style="italic",
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )