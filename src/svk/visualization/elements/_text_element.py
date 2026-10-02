from pydantic import PrivateAttr, model_validator

from svk.visualization.elements._visual_element import VisualElement
from svk.visualization.helpers._measuretext import measure_text

from svgwrite import Drawing


class TextElement(VisualElement):
    text: str
    font_family: str = "Arial"
    font_weight: str = "normal"
    font_style: str = "normal"
    text_anchor: str = "start"
    dominant_baseline: str = "text-before-edge"

    _height: float = PrivateAttr()
    _width: float = PrivateAttr()

    @model_validator(mode="after")
    def validate(self):
        self._width = measure_text(self.text, self.layout_configuration.font_size)[0]
        self._height = self.layout_configuration.font_size * 1.2
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
                self.text,
                insert=(x, y),
                font_size=self.layout_configuration.font_size,
                font_family=self.font_family,
                font_weight=self.font_weight,
                font_style=self.font_style,
                text_anchor=self.text_anchor,
                dominant_baseline=self.dominant_baseline,
            )
        )
