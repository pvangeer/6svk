from svgwrite import Drawing
from pydantic import PrivateAttr, model_validator
from svk.visualization.elements._visual_element import VisualElement
from svk.visualization.helpers._wrappedtext import wrapped_text, wrapped_lines

class WrappedBulletListElement(VisualElement):
    max_width: float
    bullet_list: list[str]

    _height: float = PrivateAttr()
    _width: float = PrivateAttr()
    
    @model_validator(mode="after")
    def validate(self):
        self._width = self.max_width
        self._height = self.layout_configuration.small_margin
        for bullet in self.bullet_list:
            lines = wrapped_lines(bullet, max_width=self.max_width - self.layout_configuration.bullet_list_indent, font_size=self.layout_configuration.font_size)
            self._height += len(lines) * self.layout_configuration.font_size * 1.2
        self._height += self.layout_configuration.small_margin
        return self
    
    @property
    def height(self) -> float:
        return self._height

    @property
    def width(self) -> float:
        return self._width

    def draw(self, dwg: Drawing, x: float, y: float) -> None:
        y_current = y + self.layout_configuration.small_margin
        if len(self.bullet_list) == 1 and self.bullet_list[0] == "-":
            dwg.add(
                dwg.text(
                    "-",
                    insert=(
                        x + self.layout_configuration.small_margin,
                        y_current
                    ),
                    font_size=self.layout_configuration.font_size,
                    text_anchor="start",
                    dominant_baseline="text-before-edge",
                )
            )
            return
        
        for bullet in self.bullet_list:
            dwg.add(
                dwg.text(
                    self.layout_configuration.bullet_character,
                    insert=(
                        x + self.layout_configuration.small_margin,
                        y_current
                    ),
                    font_size=self.layout_configuration.font_size,
                    text_anchor="start",
                    dominant_baseline="text-before-edge",
                )
            )
            
            lines = wrapped_lines(bullet, max_width=self.max_width - self.layout_configuration.bullet_list_indent, font_size=self.layout_configuration.font_size)
            dwg.add(
                wrapped_text(
                    dwg,
                    lines=lines,
                    insert=(
                        x + self.layout_configuration.bullet_list_indent + self.layout_configuration.small_margin,
                        y_current,
                    ),
                    text_anchor="start",
                    dominant_baseline="text-before-edge",
                )
            )
            y_current += len(lines) * self.layout_configuration.font_size * 1.2