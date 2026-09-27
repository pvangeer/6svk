"""
Copyright (C) Stichting Deltares 2026. All rights reserved.

This file is part of the 6svk toolbox.

This program is free software; you can redistribute it and/or modify it under the terms of
the GNU Lesser General Public License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with this
program; if not, see <https://www.gnu.org/licenses/>.

All names, logos, and references to "Deltares" are registered trademarks of Stichting
Deltares and remain full property of Stichting Deltares at all times. All rights reserved.
"""

from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict


class Color(BaseModel):
    """
    Represents a color in RGB format.

    Attributes:
        r (int): Red component (0-255).
        g (int): Green component (0-255).
        b (int): Blue component (0-255).
    """

    model_config = ConfigDict(frozen=True)
    include_hash: bool = Field(default=True)
    a: int = Field(ge=0, le=255, default=255)
    r: int = Field(ge=0, le=255)
    g: int = Field(ge=0, le=255)
    b: int = Field(ge=0, le=255)

    def __str__(self) -> str:
        """
        Returns the string representation of the color in 'rgb(r,g,b)' format.

        Returns:
            str: The string representation of the color.
        """
        return f"rgb({self.r},{self.g},{self.b})"

    def to_hex(self, include_alpha: bool = False) -> str:
        """
        Converts the RGB color to its hexadecimal representation.

        Returns:
            str: The hexadecimal representation of the color in 'RRGGBB' format.
        """
        value = f"{self.a:02X}{self.r:02X}{self.g:02X}{self.b:02X}" if include_alpha else f"{self.r:02X}{self.g:02X}{self.b:02X}"
        return f"#{value}" if self.include_hash else value

    @classmethod
    def from_hex(cls, value: str) -> Color:
        """
        Creates a Color from:

        RRGGBB
        #RRGGBB
        AARRGGBB
        #AARRGGBB

        The alpha channel, when present, is ignored.
        """
        value = value.strip().lstrip("#")

        if len(value) == 6:
            return cls(
                a=0,
                r=int(value[0:2], 16),
                g=int(value[2:4], 16),
                b=int(value[4:6], 16),
            )

        if len(value) == 8:
            return cls(
                a=int(value[0:2], 16),
                r=int(value[2:4], 16),
                g=int(value[4:6], 16),
                b=int(value[6:8], 16),
            )

        raise ValueError(f"Invalid colour value: {value}")


class KnownColors:
    White = Color(r=255, g=255, b=255)
    Black = Color(r=0, g=0, b=0)
    Red = Color(r=255, g=0, b=0)
    Blue = Color(r=0, g=0, b=255)
    Green = Color(r=0, g=255, b=0)
    Yellow = Color(r=255, g=255, b=102)
    Orange = Color(r=255, g=192, b=0)
