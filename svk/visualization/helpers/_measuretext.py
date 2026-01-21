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

from PIL import ImageFont
import os


def measure_text(text: str, font_size: int):
    """
    Returns the predicted width and height of a given text in pixels.

    Parameters:
        text (str): The text to measure.
        font_path (str): Path to the .ttf font file (e.g., Arial.ttf).
        font_size (int): Font size in pixels.

    Returns:
        (width, height): Tuple of predicted text dimensions in pixels.
    """

    font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), "ARIAL.TTF"), font_size)

    # This requires pillow >= 8.0. Otherwise we should use font.getsize(text)
    bbox = font.getbbox(text)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]

    return width, height
