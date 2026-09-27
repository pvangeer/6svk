from pydantic import BaseModel
from enum import Enum
from svk.data._color import Color, KnownColors


class IconElementType(Enum):
    Path = 0
    Rect = 1


class IconElement(BaseModel):
    type: IconElementType


class PathIconElement(IconElement):
    type: IconElementType = IconElementType.Path

    d: str
    """The path definition (definition of strokes)"""
    fill: Color = KnownColors.NoneColor
    """The fill color to be used"""
    transform: str | None = None
    """Any transformation to be applied."""
    stroke: Color = KnownColors.Black
    """The stroke color to be used."""
    stroke_linecap: str = "round"
    """Stroke linecap to be used"""
    stroke_linejoin: str = "round"
    """Stroke linejoin to be used"""
    stroke_width: float = 20.0
    """Stroke width"""


class RectIconElement(IconElement):
    type: IconElementType = IconElementType.Rect

    x: float
    """x-position of the Rect"""
    y: float
    """y-position of the Rect"""
    width: float
    """Width of the Rect"""
    height: float
    """Height of the Rect"""
    stroke: Color = KnownColors.Black
    """Stroke color to be used"""
    stroke_width: float = 20
    """Stroke width to be used"""
    strok_linejoin: str = "round"
    """Stroke linejoin to be used"""
    stroke_linecap: str = "round"
    """Stroke linecap to be used"""
    fill: Color = KnownColors.Black
    """Fill color to be used"""


class Icon(BaseModel):
    id: str
    elements: tuple[IconElement, ...]
