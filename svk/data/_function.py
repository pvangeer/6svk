from pydantic import BaseModel


class Function(BaseModel):
    """
    Class that represents a function in the EFL reader database. It is used to store the data in a structured way.
    """

    name: str
    category: str
