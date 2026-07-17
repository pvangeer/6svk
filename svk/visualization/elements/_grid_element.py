from pydantic import model_validator, PrivateAttr
from uuid import uuid4
from svgwrite import Drawing
from svk.data import Grid
from svk.visualization.helpers._greyfraction import color_toward_grey
from svk.visualization.elements._visual_elements_container import VisualElementsContainer
from svk.visualization.elements._grid_cell_element import GridCellElement
from svk.visualization.elements._grid_header_element import GridHeaderElement, HeaderOrientation


class GridElement(VisualElementsContainer):
    grid: Grid

    _row_header_elements: list[GridHeaderElement] = PrivateAttr()
    _column_header_elements: list[GridHeaderElement] = PrivateAttr()
    _cell_elements: list[GridCellElement] = PrivateAttr()

    @model_validator(mode="after")
    def validate(self):
        self._categories = list(dict.fromkeys(header.category for header in self.grid.column_headers))
        self._cell_elements = [
            GridCellElement(
                layout_configuration=self.layout_configuration,
                translator=self.translator,
                links_register=self.links_register,
                fill=c.color,
                i_row=c.i_row,
                i_column=c.i_column,
            )
            for c in self.grid.cells
        ]

        self._row_header_elements = [
            GridHeaderElement(
                layout_configuration=self.layout_configuration,
                translator=self.translator,
                links_register=self.links_register,
                label=r.label,
                orientation=HeaderOrientation.Horizontal,
                i_position=r.i_position,
            )
            for r in self.grid.row_headers
            if r.label is not None
        ]

        self._column_header_elements = [
            GridHeaderElement(
                layout_configuration=self.layout_configuration,
                translator=self.translator,
                links_register=self.links_register,
                label=c.label,
                orientation=HeaderOrientation.Vertical,
                i_position=c.i_position,
            )
            for c in self.grid.column_headers
            if c.label is not None
        ]

        self._cell_width = max(
            [(c.width + 2 * self.layout_configuration.grid_cell_margin) for c in self._column_header_elements]
            + [self.layout_configuration.grid_cell_minimal_width + 2 * self.layout_configuration.grid_cell_margin]
        )
        self._cell_height = max(
            [(f.height + 2 * self.layout_configuration.grid_cell_margin) for f in self._row_header_elements]
            + [self.layout_configuration.grid_cell_minimal_height + 2 * self.layout_configuration.grid_cell_margin]
        )
        self._top_header_height = max([d.height for d in self._column_header_elements]) + 2 * self.layout_configuration.small_margin
        self._left_header_width = max([d.width for d in self._row_header_elements]) + 2 * self.layout_configuration.small_margin

        self._x_column_starts = {}
        x_current = self._left_header_width + self.layout_configuration.small_margin
        self._category_info = {}
        for header in self.grid.column_headers:
            if header.category not in self._category_info.keys():
                if self._category_info:
                    x_current += self.layout_configuration.grid_cell_margin * 4
                category_header_positions = [h.i_position for h in self.grid.column_headers if h.category == header.category]
                self._category_info[header.category] = (
                    x_current - self.layout_configuration.grid_cell_margin,
                    len(category_header_positions) * self._cell_width + 2 * self.layout_configuration.grid_cell_margin,
                    category_header_positions,
                )

            self._x_column_starts[header.i_position] = x_current
            x_current += self._cell_width

        self._width = (
            self._left_header_width
            + self.layout_configuration.small_margin
            + self._cell_width * self.grid.n_columns
            + len(self._categories) * self.layout_configuration.grid_cell_margin * 3
            - self.layout_configuration.grid_cell_margin
        )
        self._height = (
            self.layout_configuration.font_size * 1.2
            + 2 * self.layout_configuration.small_margin
            + self._top_header_height
            + self.layout_configuration.small_margin
            + self._cell_height * self.grid.n_rows
            + self.layout_configuration.small_margin
        )
        return self

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    def draw(self, dwg: Drawing, x: float, y: float) -> None:
        for category in self._category_info.keys():
            width = self._category_info[category][1]
            height = self.height
            left = x + self._category_info[category][0]
            top = y
            color = (70, 80, 90)

            fill_gradient_id = f"gradient_{str(uuid4())}"
            fill_gradient = dwg.linearGradient(
                start=(0, 0),
                end=(0, 1),
                id=fill_gradient_id,
            )
            fill_gradient.add_stop_color(0, color_toward_grey(color, 0.5, grey=(250, 250, 250)))
            fill_gradient.add_stop_color(0.4, color_toward_grey(color, 0.8, grey=(250, 250, 250)))
            fill_gradient.add_stop_color(1, "white")

            stroke_gradient_id = f"gradient_{str(uuid4())}"
            stroke_gradient = dwg.linearGradient(
                start=(0, 0),
                end=(0, 1),
                id=stroke_gradient_id,
            )
            stroke_gradient.add_stop_color(0, color_toward_grey(color, 0.0))
            fill_gradient.add_stop_color(0.4, color_toward_grey(color, 0.8, grey=(250, 250, 250)))
            stroke_gradient.add_stop_color(1, "white")

            dwg.defs.add(fill_gradient)
            dwg.defs.add(stroke_gradient)

            dwg.add(
                dwg.rect(
                    insert=(left, top),
                    size=(width, height),
                    fill=f"url(#{fill_gradient_id})",  # TODO: Relate to categoyr
                    stroke=f"url(#{stroke_gradient_id})",
                    stroke_width=1,
                )
            )
            self.draw_horizontal_separator(
                dwg=dwg,
                x=left,
                y=y + self.layout_configuration.font_size * 1.2 + 2 * self.layout_configuration.small_margin,
                element_width=self._category_info[category][1],
                color="#708090",
            )
            dwg.add(
                dwg.text(
                    category,
                    x=[left + self._category_info[category][1] / 2.0],
                    y=[y + self.layout_configuration.font_size * 0.6 + self.layout_configuration.small_margin],
                    font_size=self.layout_configuration.font_size,
                    fill="white",
                    font_family="Arial",
                    font_weight="normal",
                    font_style="italic",
                    text_anchor="middle",
                    dominant_baseline="central",
                )
            )

        category_row_height = 2 * self.layout_configuration.small_margin + self.layout_configuration.font_size * 1.2
        for _column_header in self._column_header_elements:
            _column_header.draw(
                dwg=dwg,
                x=x + self._x_column_starts[_column_header.i_position] + self._cell_width / 2.0,
                y=y + category_row_height + self._top_header_height - self.layout_configuration.small_margin,
            )

        for _row_header in self._row_header_elements:
            _row_header.draw(
                dwg=dwg,
                x=x + self._left_header_width - self.layout_configuration.small_margin,
                y=y
                + category_row_height
                + self._top_header_height
                + self.layout_configuration.small_margin
                + self._cell_height * _row_header.i_position
                - self._cell_height / 2.0,
            )

        for _cell_element in self._cell_elements:
            _cell_element.draw(
                dwg=dwg,
                x=x + self._x_column_starts[_cell_element.i_column] + (self._cell_width - _cell_element.width) / 2.0,
                y=y
                + category_row_height
                + self._top_header_height
                + self.layout_configuration.small_margin
                + (_cell_element.i_row - 1) * self._cell_height
                + (self._cell_height - _cell_element.height) / 2.0,
            )
