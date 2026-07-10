from svk.visualization.pages._page import Page
from svgwrite import Drawing
from pydantic import PrivateAttr, model_validator
from svk.io._endoflifedatabase import Function, Driver, EndOfLifeCell
from svk.visualization.elements._grid_header_element import GridHeaderElement, HeaderOrientation
from svk.visualization.elements._grid_cell_element import GridCellElement


class EndOfLifePage(Page):
    functions: list[Function]
    drivers: list[Driver]
    cells: list[EndOfLifeCell]

    _height: float = PrivateAttr()
    _width: float = PrivateAttr()
    _driver_elements: list[GridHeaderElement] = PrivateAttr()
    _function_elements: list[GridHeaderElement] = PrivateAttr()
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
            for c in self.cells
        ]
        self._function_elements = [
            GridHeaderElement(
                layout_configuration=self.layout_configuration,
                translator=self.translator,
                links_register=self.links_register,
                label=f.name,
                orientation=HeaderOrientation.Horizontal,
            )
            for f in self.functions
        ]
        self._driver_elements = [
            GridHeaderElement(
                layout_configuration=self.layout_configuration,
                translator=self.translator,
                links_register=self.links_register,
                label=d.name,
                orientation=HeaderOrientation.Vertical,
            )
            for d in self.drivers
        ]

        self._cell_width = max([d.width for d in self._driver_elements] + [self.layout_configuration.grid_cell_minimal_width])
        self._cell_height = max([f.height for f in self._function_elements] + [self.layout_configuration.grid_cell_minimal_height])

        self._width = (
            max([f.width for f in self._function_elements])
            + 2 * self.layout_configuration.small_margin
            + (self._cell_width + self.layout_configuration.small_margin) * len(self._driver_elements)
            + self.layout_configuration.small_margin
        )
        self._height = (
            max([d.height for d in self._driver_elements])
            + 2 * self.layout_configuration.small_margin
            + (self._cell_height + self.layout_configuration.small_margin) * len(self._function_elements)
            + self.layout_configuration.small_margin
        )
        return self

    def get_content_size(self) -> tuple[float, float]:
        return (self._width, self._height)

    def draw_content(self, dwg: Drawing, left: float, top: float):
        first_row_height = max([d.height for d in self._driver_elements])
        first_column_width = max([e.width for e in self._function_elements])

        current_left = left
        current_top = top + first_row_height + 2 * self.layout_configuration.small_margin
        for function_element in self._function_elements:
            function_element.draw(dwg, current_left, current_top)
            current_top += self.layout_configuration.small_margin + self._cell_height

        current_top = top + first_row_height
        current_left = left + first_column_width + 2 * self.layout_configuration.small_margin
        for driver_element in self._driver_elements:
            driver_element.draw(dwg, current_left, current_top)
            current_left += self.layout_configuration.small_margin + self._cell_width

        current_top = top + first_row_height + 2 * self.layout_configuration.small_margin
        current_left = left + first_column_width + 2 * self.layout_configuration.small_margin
        for cell_element in self._cell_elements:
            l = current_left + (cell_element.i_column - 4) * (self._cell_width + self.layout_configuration.small_margin)
            t = current_top + (cell_element.i_row - 4) * (self._cell_height + self.layout_configuration.small_margin)
            cell_element.draw(dwg, l, t)
