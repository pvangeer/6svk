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
import re
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
    no_color: bool = Field(default=False)
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
        return self.to_rgb()

    def to_rgb(self) -> str:
        """
        Returns the string representation of the color in 'rgb(r,g,b)' format.

        Returns:
            str: The string representation of the color.
        """
        if self.no_color:
            return "none"

        return f"rgb({self.r},{self.g},{self.b})"

    def to_hex(self, include_alpha: bool = False) -> str:
        """
        Converts the RGB color to its hexadecimal representation.

        Returns:
            str: The hexadecimal representation of the color in 'RRGGBB' format.
        """
        if self.no_color:
            raise ValueError("Color components must be set to convert to hex.")

        value = f"{self.a:02X}{self.r:02X}{self.g:02X}{self.b:02X}" if include_alpha else f"{self.r:02X}{self.g:02X}{self.b:02X}"
        return f"#{value}" if self.include_hash else value

    @classmethod
    def from_str(cls, value: str) -> Color:
        """
        Creates a Color from one of the following formats:

            none
            RRGGBB
            #RRGGBB
            AARRGGBB
            #AARRGGBB
            rgb(r, g, b)
            rgba(r, g, b, alpha)

        Eight-digit hexadecimal values use the AARRGGBB format.

        The alpha component in rgba() may be:
            - A floating-point value from 0.0 to 1.0
            - An integer from 0 to 255
            - A percentage from 0% to 100%
        """
        if not isinstance(value, str):
            raise TypeError(f"Color value must be a string, not {type(value).__name__}.")

        value = value.strip()

        if value.casefold() == "none":
            return cls(no_color=True, r=0, g=0, b=0)

        # Hex: RRGGBB or AARRGGBB
        hex_match = re.fullmatch(
            r"#?([0-9a-fA-F]{6}|[0-9a-fA-F]{8})",
            value,
        )

        if hex_match:
            hex_value = hex_match.group(1)

            if len(hex_value) == 6:
                return cls(
                    a=255,
                    r=int(hex_value[0:2], 16),
                    g=int(hex_value[2:4], 16),
                    b=int(hex_value[4:6], 16),
                )

            return cls(
                a=int(hex_value[0:2], 16),
                r=int(hex_value[2:4], 16),
                g=int(hex_value[4:6], 16),
                b=int(hex_value[6:8], 16),
            )

        # RGB: rgb(r, g, b)
        rgb_match = re.fullmatch(
            r"rgb\s*\(\s*" r"(\d{1,3})\s*,\s*" r"(\d{1,3})\s*,\s*" r"(\d{1,3})" r"\s*\)",
            value,
            re.IGNORECASE,
        )

        if rgb_match:
            r, g, b = map(int, rgb_match.groups())

            cls._validate_rgb_components(r, g, b, value)

            return cls(
                a=255,
                r=r,
                g=g,
                b=b,
            )

        # RGBA: rgba(r, g, b, alpha)
        rgba_match = re.fullmatch(
            r"rgba\s*\(\s*" r"(\d{1,3})\s*,\s*" r"(\d{1,3})\s*,\s*" r"(\d{1,3})\s*,\s*" r"(\d+(?:\.\d+)?%?)" r"\s*\)",
            value,
            re.IGNORECASE,
        )

        if rgba_match:
            r = int(rgba_match.group(1))
            g = int(rgba_match.group(2))
            b = int(rgba_match.group(3))
            alpha_value = rgba_match.group(4)

            cls._validate_rgb_components(r, g, b, value)

            if alpha_value.endswith("%"):
                percentage = float(alpha_value[:-1])

                if not 0 <= percentage <= 100:
                    raise ValueError(f"Alpha percentage must be between 0% and 100%: " f"{alpha_value}")

                a = round(percentage * 255 / 100)

            elif "." in alpha_value:
                opacity = float(alpha_value)

                if not 0.0 <= opacity <= 1.0:
                    raise ValueError(f"A decimal alpha value must be between 0.0 and 1.0: " f"{alpha_value}")

                a = round(opacity * 255)

            else:
                a = int(alpha_value)

                if not 0 <= a <= 255:
                    raise ValueError(f"An integer alpha value must be between 0 and 255: " f"{alpha_value}")

            return cls(
                a=a,
                r=r,
                g=g,
                b=b,
            )

        raise ValueError(f"Invalid colour value: {value!r}")

    @staticmethod
    def _validate_rgb_components(
        r: int,
        g: int,
        b: int,
        original_value: str,
    ) -> None:
        for name, component in (("r", r), ("g", g), ("b", b)):
            if not 0 <= component <= 255:
                raise ValueError(f"Component {name} must be between 0 and 255 in " f"{original_value!r}; received {component}.")


class KnownColors:
    White = Color(r=255, g=255, b=255)
    Black = Color(r=0, g=0, b=0)
    Red = Color(r=255, g=0, b=0)
    Blue = Color(r=0, g=0, b=255)
    DefaultBlue = Color(r=18, g=103, b=221)
    Green = Color(r=0, g=255, b=0)
    Yellow = Color(r=255, g=255, b=102)
    Orange = Color(r=255, g=192, b=0)
    GreyAccent = Color(r=167, g=167, b=167)
    LightGrey = Color(r=210, g=210, b=210)
    NoneColor = Color(no_color=True, r=0, g=0, b=0)

    Orange = Color(r=233, g=113, b=50)
    LightGreen = Color(r=142, g=178, b=30)
    DarkGreen = Color(r=25, g=107, b=36)

    RWSBlue1 = Color.from_str("#103156")  # rgb(16, 49, 86)
    RWSBlue2 = Color.from_str("#418BDC")  # rgb(65, 139, 220)
    RWSBlue3 = Color.from_str("#C0D8F3")  # rgb(192, 216, 243)
    RWSYellow1 = Color.from_str("#6B6003")  # rgb(107, 96, 3)
    RWSYellow2 = Color.from_str("#CCB705")  # rgb(204, 183, 5)
    RWSYellow3 = Color.from_str("#FDF3A5")  # rgb(253, 243, 165)
    RWSGrey1 = Color.from_str("#7F7F7F")  # rgb(127, 127, 127)
    RWSGrey2 = Color.from_str("#BFBFBF")  # rgb(191, 191, 191)
    RWSGrey3 = Color.from_str("#F2F2F2")  # rgb(242, 242, 242)
