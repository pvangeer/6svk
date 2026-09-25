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
from svk.data.helpers import color_toward_grey
from svk.visualization._layout_configuration import LayoutConfiguration


def get_contrast_color(background_rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    """Returns (0, 0, 0) or (255, 255, 255)."""

    r, g, b = [c / 255.0 for c in background_rgb]

    def linearize(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r = linearize(r)
    g = linearize(g)
    b = linearize(b)

    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b

    contrast_white = (1.05) / (luminance + 0.05)
    contrast_black = (luminance + 0.05) / 0.05

    return (255, 255, 255) if contrast_white > contrast_black else (0, 0, 0)


def get_text_color(time_frame: TimeFrame, research_line_group: int | None = None) -> str:
    if research_line_group is None:
        return "black"
    else:
        match time_frame:
            case TimeFrame.Now:
                return "white"
            case _:
                return "black"


def color_to_string(color: tuple[int, int, int]) -> str:
    return f"rgb({color[0]},{color[1]},{color[2]})"


def get_color(layout_configuration: LayoutConfiguration, time_frame: TimeFrame, research_line_group: int | None = None) -> str:
    if layout_configuration.use_rijkswaterstaat_colors and research_line_group is not None:
        return color_to_string(get_rijkswaterstaat_style_color(time_frame, research_line_group))
    else:
        return get_color_toward_grey(time_frame)


def get_color_toward_grey(time_frame: TimeFrame) -> str:
    return color_toward_grey((18, 103, 221), grey_fraction=time_frame.grey_fraction)


def get_rijkswaterstaat_style_color(time_frame: TimeFrame, research_line_group: int) -> tuple[int, int, int]:
    match (time_frame, research_line_group):
        case (TimeFrame.Now, 1):
            return (16, 49, 86)
        case (TimeFrame.Now, 2):
            return (107, 96, 3)
        case (TimeFrame.Now, 3):
            return (127, 127, 127)
        case (TimeFrame.NearFuture, 1):
            return (65, 139, 220)
        case (TimeFrame.NearFuture, 2):
            return (204, 183, 5)
        case (TimeFrame.NearFuture, 3):
            return (191, 191, 191)
        case (TimeFrame.Future, 1):
            return (192, 216, 243)
        case (TimeFrame.Future, 2):
            return (253, 243, 165)
        case (TimeFrame.Future, 3):
            return (242, 242, 242)
        case _:
            return (18, 103, 221)


def rgb_string_to_tuple(rgb_string: str) -> tuple[int, int, int]:
    values = rgb_string.removeprefix("rgb(").removesuffix(")")
    r, g, b = map(int, values.split(","))
    return r, g, b
