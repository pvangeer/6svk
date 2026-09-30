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


def get_color(layout_configuration: LayoutConfiguration, time_frame: TimeFrame, research_line_group: int | None = None) -> Color:
    if layout_configuration.use_rijkswaterstaat_colors and research_line_group is not None:
        return get_rijkswaterstaat_style_color(time_frame, research_line_group)
    else:
        return get_blue_toward_grey(time_frame)


def get_blue_toward_grey(time_frame: TimeFrame) -> Color:
    return color_toward_grey(Color.from_str("#1267DD"), grey_fraction=time_frame.grey_fraction)


def get_rijkswaterstaat_style_color(time_frame: TimeFrame, research_line_group: int) -> Color:
    match (time_frame, research_line_group):
        case (TimeFrame.Now, 1):
            return Color.from_str("#103156")  # rgb(16, 49, 86)
        case (TimeFrame.Now, 2):
            return Color.from_str("#6B6003")  # rgb(107, 96, 3)
        case (TimeFrame.Now, 3):
            return Color.from_str("#7F7F7F")  # rgb(127, 127, 127)

        case (TimeFrame.NearFuture, 1):
            return Color.from_str("#418BDC")  # rgb(65, 139, 220)
        case (TimeFrame.NearFuture, 2):
            return Color.from_str("#CCB705")  # rgb(204, 183, 5)
        case (TimeFrame.NearFuture, 3):
            return Color.from_str("#BFBFBF")  # rgb(191, 191, 191)

        case (TimeFrame.Future, 1):
            return Color.from_str("#C0D8F3")  # rgb(192, 216, 243)
        case (TimeFrame.Future, 2):
            return Color.from_str("#FDF3A5")  # rgb(253, 243, 165)
        case (TimeFrame.Future, 3):
            return Color.from_str("#F2F2F2")  # rgb(242, 242, 242)

        case _:
            return Color.from_str("#1267DD")  # rgb(18, 103, 221)
