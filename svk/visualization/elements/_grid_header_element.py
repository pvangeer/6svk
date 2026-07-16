from svgwrite import Drawing
from pydantic import PrivateAttr, model_validator
from svk.visualization.helpers._measuretext import measure_text
from svk.visualization.helpers._wrappedtext import wrapped_lines, wrapped_text
from svk.visualization.elements._visual_element import VisualElement
from enum import Enum


class HeaderOrientation(Enum):
    Vertical = False
    Horizontal = True


class GridHeaderElement(VisualElement):
    label: str
    color: str | None = None  # TODO: Also include a background and include color in drawing/size?
    orientation: HeaderOrientation
    i_position: int

    _height: float = PrivateAttr()
    _width: float = PrivateAttr()
    _lines: list[str] = PrivateAttr()

    @model_validator(mode="after")
    def validate(self):
        self._lines = wrapped_lines(text=self.label, max_width=200, font_size=self.layout_configuration.font_size)

        if self.orientation.value:
            self._width = max([measure_text(text=l, font_size=self.layout_configuration.font_size)[0] for l in self._lines])
            self._height = len(self._lines) * self.layout_configuration.font_size * 1.2
        else:
            self._width = len(self._lines) * self.layout_configuration.font_size * 1.2
            self._height = max([measure_text(text=l, font_size=self.layout_configuration.font_size)[0] for l in self._lines])
        return self

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    def draw(self, dwg: Drawing, x: float, y: float):
        if self.orientation == HeaderOrientation.Vertical:
            text_element = wrapped_text(
                dwg=dwg,
                lines=self._lines,
                insert=(x, y),
                font_size=self.layout_configuration.font_size,
                font_family="Arial",
                font_weight="normal",
                text_anchor="start",
                dominant_baseline="mathematical",
            )
            text_element.rotate(-90, center=(x, y))
            dwg.add(text_element)
        else:
            dwg.add(
                wrapped_text(
                    dwg=dwg,
                    lines=self._lines,
                    insert=(x, y),
                    font_size=self.layout_configuration.font_size,
                    font_family="Arial",
                    font_weight="normal",
                    text_anchor="end",
                    dominant_baseline="text-after-edge",
                )
            )
