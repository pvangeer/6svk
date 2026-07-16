from pydantic import model_validator, PrivateAttr
from svgwrite import Drawing
from svk.data import Grid
from svk.visualization.elements._visual_elements_container import VisualElementsContainer, Alignment
from svk.visualization.elements._grid_cell_element import GridCellElement
from svk.visualization.elements._grid_header_element import GridHeaderElement, HeaderOrientation


class GridElement(VisualElementsContainer):
    grid: Grid

    _row_header_elements: list[GridHeaderElement] = PrivateAttr()
    _column_header_elements: list[GridHeaderElement] = PrivateAttr()
    _cell_elements: list[GridCellElement] = PrivateAttr()

    @model_validator(mode="after")
    def validate(self):
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

        self._width = self._left_header_width + self._cell_width * self.grid.n_columns
        self._height = self._top_header_height + self._cell_height * self.grid.n_rows
        return self

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    def draw(self, dwg: Drawing, x: float, y: float) -> None:
        unique_categories = list(dict.fromkeys(header.category for header in self.grid.column_headers))
        self.draw_vertical_separator(dwg=dwg, x=x + self._left_header_width, y=y, element_height=self.height, color="#FF0000")
        for _column_header in self._column_header_elements:
            _column_header.draw(
                dwg=dwg,
                x=x
                + self._left_header_width
                + self.layout_configuration.small_margin
                + (_column_header.i_position) * self._cell_width
                - self._cell_width / 2.0,
                y=y + self._top_header_height - self.layout_configuration.small_margin,
            )
            self.draw_vertical_separator(
                dwg=dwg,
                x=x
                + self._left_header_width
                + self.layout_configuration.small_margin
                + (_column_header.i_position) * self._cell_width
                - self._cell_width / 2.0,
                y=y,
                element_height=self.height,
                color="#00FF00",
            )

        self.draw_horizontal_separator(dwg=dwg, x=x, y=y + self._top_header_height, element_width=self.width, color="#FF0000")
        for _row_header in self._row_header_elements:
            _row_header.draw(
                dwg=dwg,
                x=x + self._left_header_width - self.layout_configuration.small_margin,
                y=y
                + self._top_header_height
                + self.layout_configuration.small_margin
                + self._cell_height * _row_header.i_position
                - self._cell_height / 2.0,
            )
            self.draw_horizontal_separator(
                dwg=dwg,
                x=x,
                y=y
                + self._top_header_height
                + self.layout_configuration.small_margin
                + _row_header.i_position * self._cell_height
                - self._cell_height / 2.0,
                element_width=self.width,
                color="#00FF00",
            )

        for _cell_element in self._cell_elements:
            _cell_element.draw(
                dwg=dwg,
                x=x
                + self._left_header_width
                + self.layout_configuration.small_margin
                + (_cell_element.i_column - 1) * self._cell_width
                + (self._cell_width - _cell_element.width) / 2.0,
                y=y
                + self._top_header_height
                + self.layout_configuration.small_margin
                + (_cell_element.i_row - 1) * self._cell_height
                + (self._cell_height - _cell_element.height) / 2.0,
            )
