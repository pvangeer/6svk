from pydantic import BaseModel

# TODO: Optimize etc.


class LayoutConfiguration(BaseModel):
    # Margins
    paper_margin: float = 20
    element_margin: float = 10.0
    line_margin: float = 5.0

    # Font sizes
    figure_title_font_size: int = 64
    column_header_font_size: int = 18
    group_title_font_size: int = 14
    font_size: int = 12
    disclamer_font_size: int = 8

    # Sizes
    arrow_depth: float = 20
    figure_title_height: int = 80
    column_header_height: int = 60
    group_header_height: int = 30

    question_max_width: float = 570  # TODO: Progress or derive
    column_width: int = 650
    header_width: int = 650
    priority_width: int = 15
    svk_icon_width: int = 24

    # From Figure
    group_colors: dict[int, tuple[int, int, int]] = {}
    """A dictionary with group colors."""
