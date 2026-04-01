from svgwrite import Drawing
from pydantic import PrivateAttr, model_validator
from svk.visualization.elements._visual_element import VisualElement
from svk.visualization.helpers._wrappedtext import wrapped_text, wrapped_lines


class WrappedTextElement(VisualElement):
    max_width: float
    text: str

    _height: float = PrivateAttr()
    _width: float = PrivateAttr()
    _lines: list[str] = PrivateAttr()

    @model_validator(mode="after")
    def validate(self):
        self._width = self.max_width
        self._lines = wrapped_lines(self.text, max_width=self.max_width, font_size=self.layout_configuration.font_size)
        self._height = len(self._lines) * self.layout_configuration.font_size * 1.2 + 2 * self.layout_configuration.small_margin
        return self

    @property
    def height(self) -> float:
        return self._height

    @property
    def width(self) -> float:
        return self._width

    def draw(self, dwg: Drawing, x: float, y: float) -> None:
        dwg.add(
            wrapped_text(
                dwg,
                lines=self._lines,
                insert=(
                    x + self.layout_configuration.small_margin,
                    y + self.layout_configuration.small_margin,
                ),
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )
