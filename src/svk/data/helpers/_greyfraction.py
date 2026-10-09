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
from svk.data._timeframe import TimeFrame  # tEmporarily, because we still need colors in data


def get_grey_fraction(time_frame: TimeFrame) -> float:
    match time_frame:
        case TimeFrame.NotRelevant:
            return 1
        case TimeFrame.Now:
            return 0.0
        case TimeFrame.NearFuture:
            return 0.5
        case TimeFrame.Future:
            return 0.7
        case TimeFrame.Unknown:
            return 0
        case _:
            return 1


def color_toward_grey(color: Color, grey_fraction: float = 0.5, grey: Color = Color(r=210, g=190, b=210)) -> Color:
    """
    Creates an rgb-string of a color towards another (grey) color.

    :param color: The initial color
    :type color: Color
    :param grey_fraction: The fraction (percentage) of the second color that should be part of the resulting color
    :type grey_fraction: float
    :param grey: The second (grey) color
    :type grey: Color
    :return: String representation of the resulting color
    :rtype: str
    """
    r_x = round(color.r + (grey.r - color.r) * grey_fraction)
    g_x = round(color.g + (grey.g - color.g) * grey_fraction)
    b_x = round(color.b + (grey.b - color.b) * grey_fraction)
    return Color(r=r_x, g=g_x, b=b_x)
