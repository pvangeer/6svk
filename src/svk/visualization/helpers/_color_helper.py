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

from svk.data import TimeFrame
from svk.data._color import Color, KnownColors
from svk.data.helpers import color_toward_grey
from svk.visualization._layout_configuration import LayoutConfiguration


def get_contrast_color(background_rgb: Color) -> Color:
    """Returns (0, 0, 0) or (255, 255, 255)."""

    def linearize(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r = linearize(background_rgb.r / 255.0)
    g = linearize(background_rgb.g / 255.0)
    b = linearize(background_rgb.b / 255.0)

    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b

    contrast_white = (1.05) / (luminance + 0.05)
    contrast_black = (luminance + 0.05) / 0.05

    return KnownColors.White if contrast_white > contrast_black else KnownColors.Black


def get_text_color(time_frame: TimeFrame, research_line_group: int | None = None) -> str:
    if research_line_group is None:
        return "black"
    else:
        match time_frame:
            case TimeFrame.Now:
                return "white"
            case _:
                return "black"


def get_color(layout_configuration: LayoutConfiguration, time_frame: TimeFrame, research_line_group: int | None = None) -> Color:
    if layout_configuration.use_rijkswaterstaat_colors and research_line_group is not None:
        return get_rijkswaterstaat_style_color(time_frame, research_line_group)
    else:
        return get_color_toward_grey(time_frame)


def get_color_toward_grey(time_frame: TimeFrame) -> Color:
    return color_toward_grey(Color(r=18, g=103, b=221), grey_fraction=time_frame.grey_fraction)


def get_rijkswaterstaat_style_color(time_frame: TimeFrame, research_line_group: int) -> Color:
    match (time_frame, research_line_group):
        case (TimeFrame.Now, 1):
            return Color(r=16, g=49, b=86)
        case (TimeFrame.Now, 2):
            return Color(r=107, g=96, b=3)
        case (TimeFrame.Now, 3):
            return Color(r=127, g=127, b=127)
        case (TimeFrame.NearFuture, 1):
            return Color(r=65, g=139, b=220)
        case (TimeFrame.NearFuture, 2):
            return Color(r=204, g=183, b=5)
        case (TimeFrame.NearFuture, 3):
            return Color(r=191, g=191, b=191)
        case (TimeFrame.Future, 1):
            return Color(r=192, g=216, b=243)
        case (TimeFrame.Future, 2):
            return Color(r=253, g=243, b=165)
        case (TimeFrame.Future, 3):
            return Color(r=242, g=242, b=242)
        case _:
            return Color(r=18, g=103, b=221)
