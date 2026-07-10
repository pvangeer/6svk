from bisect import bisect_right
from openpyxl.styles.fills import PatternFill
from svk.io._exceldatabase import ExcelDatabase
from svk.data import Driver, Function, Color
from pydantic import BaseModel


class EndOfLifeCell(BaseModel):
    """
    Class that represents a cell in the EFL reader database. It is used to store the data in a structured way.
    """

    i_row: int
    i_column: int
    color: Color
    driver: Driver
    function: Function
    question_references: list[str] = []


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
        self._drivers_dict: dict[int, int] = {}
        self._functions_dict: dict[int, int] = {}
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
            for i, cell in enumerate(row[3:]):
                new_driver = Driver(
                    name=str(cell.value),
                    category=self.driver_categories[
                        self._driver_column_indices[bisect_right(self._driver_column_indices, cell.column) - 1]
                    ],
                )
                self.drivers.append(new_driver)
                self._drivers_dict[id(new_driver)] = i
            return

        if row[0].value is not None:
            self._current_function_category = row[0].value

        if row[1].value is None or self._current_function_category == "":
            return

        new_function = Function(name=str(row[1].value), category=self._current_function_category)
        self.functions.append(new_function)
        self._functions_dict[id(new_function)] = i_row
        self.cells.extend(
            [
                EndOfLifeCell(
                    driver=d,
                    function=new_function,
                    question_references=str(row[self._drivers_dict[id(d)] - 1].value).split("/"),
                    color=self.fill_to_rgb(row[self._drivers_dict[id(d)] - 1].fill),
                    i_row=i_row,
                    i_column=self._drivers_dict[
                        id(d)
                    ],  # TODO: This is not the actual column in Excel, but the i when looking at the cells from D onwards
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
