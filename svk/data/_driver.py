from pydantic import BaseModel


class Driver(BaseModel):
    """
    Class that represents a driver in the EFL reader database. It is used to store the data in a structured way.
    """

    name: str
    category: str
