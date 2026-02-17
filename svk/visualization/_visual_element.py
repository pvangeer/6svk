from pydantic import BaseModel
from svk.visualization._layout_configuration import LayoutConfiguration


class VisualElement(BaseModel):
    layout_configuration: LayoutConfiguration
    """The layout configuration shared across all elements of a figure."""
