from pydantic import BaseModel

from svk.data._color import Color


class GridHeader(BaseModel):
    i_position: int
    label: str
    category: str | None = None


class GridCell(BaseModel):
    i_row: int
    i_column: int
    color: Color
    content: str | None = None


class Grid(BaseModel):
    n_rows: int
    n_columns: int
    row_headers: list[GridHeader]
    column_headers: list[GridHeader]
    cells: list[GridCell]
