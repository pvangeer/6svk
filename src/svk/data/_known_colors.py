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

from svk.data._color import Color


class KnownColors:
    White = Color.from_str("#FFFFFF")  # rgb(255, 255, 255)
    Red = Color.from_str("#FF0000")  # rgb(255, 0, 0)
    Blue = Color.from_str("#0000FF")  # rgb(0, 0, 255)
    RWSBlue1 = Color.from_str("#103156")  # rgb(16, 49, 86)
    RWSBlue2 = Color.from_str("#418BDC")  # rgb(65, 139, 220)
    RWSBlue3 = Color.from_str("#C0D8F3")  # rgb(192, 216, 243)
    DefaultBlue = Color.from_str("#0C67DD")  # rgb(18, 103, 221)
    Green = Color.from_str("#00FF00")  # rgb(0, 255, 0)
    LightGreen = Color.from_str("#8EB21E")  # rgb(142, 178, 30)
    DarkGreen = Color.from_str("#196B24")  # rgb(25, 107, 36)
    Yellow = Color.from_str("#FFFF66")  # rgb(255, 255, 102)
    RWSYellow1 = Color.from_str("#6B6003")  # rgb(107, 96, 3)
    RWSYellow2 = Color.from_str("#CCB705")  # rgb(204, 183, 5)
    RWSYellow3 = Color.from_str("#FDF3A5")  # rgb(253, 243, 165)
    Orange = Color.from_str("#FFC000")  # rgb(255, 192, 0)
    DarkOrange = Color.from_str("#E97132")  # rgb(233, 113, 50)
    RWSGrey1 = Color.from_str("#7F7F7F")  # rgb(127, 127, 127)
    RWSGrey2 = Color.from_str("#BFBFBF")  # rgb(191, 191, 191)
    RWSGrey3 = Color.from_str("#F2F2F2")  # rgb(242, 242, 242)
    LightGrey = Color.from_str("#D2D2D2")  # rgb(210, 210, 210)
    GreyAccent = Color.from_str("#A7A7A7")  # rgb(167, 167, 167)
    Black = Color.from_str("#000000")  # rgb(0, 0, 0)
    NoneColor = Color.from_str("none")  # rgb(0, 0, 0); no color
