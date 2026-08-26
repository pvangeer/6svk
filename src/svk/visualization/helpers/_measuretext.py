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

from svk.io import RendererServer


def measure_text(text: str, font_size: int) -> tuple[float, float]:
    """
    Returns the predicted width and height of a given text in pixels, based on an arial font.

    Parameters:
        text (str): The text to measure.
        font_size (int): Font size in pixels.

    Returns:
        (width, height): Tuple of predicted text dimensions in pixels.
    """

    return RendererServer.measure_text(text=text, font_size=font_size)


def measure_text_chromium(
    text: str,
    font_family: str = "Arial",
    font_size: int = 12,
    font_weight: str = "normal",
    font_style: str = "normal",
) -> tuple[float, float]:

    return RendererServer.measure_text(
        text=text, font_size=font_size, font_family=font_family, font_weight=font_weight, font_style=font_style
    )
