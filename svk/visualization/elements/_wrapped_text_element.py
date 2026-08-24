from svgwrite import Drawing
from pydantic import PrivateAttr, model_validator
from svk.visualization.elements._visual_element import VisualElement
from svk.visualization.helpers._wrappedtext import wrapped_text, wrapped_lines


class WrappedTextElement(VisualElement):
    max_width: float
    has_margins: bool = True
    text: str

    _height: float = PrivateAttr()
    _width: float = PrivateAttr()
    _lines: list[str] = PrivateAttr()

    @model_validator(mode="after")
    def validate(self):
        self._width = self.max_width
        max_text_width = self.max_width - self.layout_configuration.small_margin * 2 if self.has_margins else self.max_width
        self._lines = wrapped_lines(self.text, max_width=max_text_width, font_size=self.layout_configuration.font_size)
        self._height = (
            len(self._lines) * self.layout_configuration.font_size * 1.2 + 2 * self.layout_configuration.small_margin
            if self.has_margins
            else len(self._lines) * self.layout_configuration.font_size * 1.2
        )
        return self

    @property
    def height(self) -> float:
        return self._height

    @property
    def width(self) -> float:
        return self._width

    def draw(self, dwg: Drawing, x: float, y: float) -> None:
        x = x + self.layout_configuration.small_margin if self.has_margins else x
        y = y + self.layout_configuration.small_margin if self.has_margins else y
        dwg.add(
            wrapped_text(
                dwg,
                lines=self._lines,
                insert=(
                    x,
                    y,
                ),
                text_anchor="start",
                dominant_baseline="text-before-edge",
            )
        )
