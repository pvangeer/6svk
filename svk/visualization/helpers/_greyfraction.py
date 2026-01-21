"""
Copyright (C) Stichting Deltares 2026. All rights reserved.

This file is part of the dikernel-python toolbox.

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


def color_toward_grey(color: tuple[int, int, int], grey_fraction=0.5, grey: tuple[int, int, int] = (210, 190, 210)) -> str:
    r, g, b = color
    r2, g2, b2 = grey
    r_x = round(r + (r2 - r) * grey_fraction)
    g_x = round(g + (g2 - g) * grey_fraction)
    b_x = round(b + (b2 - b) * grey_fraction)
    return f"rgb({r_x},{g_x},{b_x})"
