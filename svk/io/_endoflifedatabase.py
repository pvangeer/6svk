from bisect import bisect_right
from openpyxl.styles.fills import PatternFill
from svk.io._exceldatabase import ExcelDatabase
from pydantic import BaseModel
from enum import Enum


class Color(Enum):
    White = "FFFFFF"
    Yellow = "FFFF66"
    Orange = "FFC000"
    Red = "FF0000"


class Driver(BaseModel):
    """
    Class that represents a driver in the EFL reader database. It is used to store the data in a structured way.
    """

    name: str
    category: str
    i_column: int


class Function(BaseModel):
    """
    Class that represents a function in the EFL reader database. It is used to store the data in a structured way.
    """

    name: str
    category: str
    i_row: int


class EndOfLifeCell(BaseModel):
    """
    Class that represents a cell in the EFL reader database. It is used to store the data in a structured way.
    """

    driver: Driver
    function: Function
    question_references: list[str] = []
    color: Color


class EndOfLifeDatabase(ExcelDatabase):
    """
    Class that represents the EFL database. It is used to read the database file and store the data in a
    structured way.
    """

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.first_data_row = 1
        self.sheet_name = "EFL"
        self.driver_categories: dict[int, str] = {}
        self._current_function_category: str = "Onbekend"
        self.drivers: list[Driver] = []
        self.functions: list[Function] = []
        self.cells: list[EndOfLifeCell] = []

    def read_and_append_row(self, row, i_row: int) -> None:
        """
        Reads the database file and stores the data in a structured way.

        :param self: The Database object
        :return: None
        :rtype: None
        """
        if i_row == self.first_data_row:
            self.driver_categories[0] = "Autonome situatie"
            for c in row[3:]:
                if c.value is not None:
                    self.driver_categories[c.column] = c.value

            self._driver_column_indices = [k for k in self.driver_categories.keys()]
            return

        if i_row == self.first_data_row + 1:
            self.drivers = [
                Driver(
                    name=str(cell.value),
                    category=self.driver_categories[
                        self._driver_column_indices[bisect_right(self._driver_column_indices, cell.column) - 1]
                    ],
                    i_column=cell.column,
                )
                for i, cell in enumerate(row[3:])
                if str(cell.value) != "Drivers"
            ]
            return

        if row[0].value is not None:
            self._current_function_category = row[0].value

        if row[1].value is None or self._current_function_category == "":
            return

        current_function = Function(name=str(row[1].value), category=self._current_function_category, i_row=i_row)
        self.functions.append(current_function)
        self.cells.extend(
            [
                EndOfLifeCell(
                    driver=d,
                    function=current_function,
                    question_references=str(row[d.i_column - 1].value).split("/"),
                    color=self.fill_to_rgb(row[d.i_column - 1].fill),
                )
                for d in self.drivers
            ]
        )

    @staticmethod
    def fill_to_rgb(fill: PatternFill) -> Color:
        color = fill.fgColor

        rgb = "FFFFFF"
        if color.type == "rgb" and color.rgb:
            rgb = color.rgb[2:] if len(color.rgb) == 8 else color.rgb

        match rgb:
            case Color.White.value:
                return Color.White
            case Color.Yellow.value:
                return Color.Yellow
            case Color.Orange.value:
                return Color.Orange
            case Color.Red.value:
                return Color.Red
            case _:
                return Color.White
