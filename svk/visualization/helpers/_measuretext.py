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

from playwright.sync_api import sync_playwright
from PIL import ImageFont
import os


def measure_text(text: str, font_size: int):
    """
    Returns the predicted width and height of a given text in pixels, based on an arial font.

    Parameters:
        text (str): The text to measure.
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


def measure_text_chromium(
    text: str,
    font_family: str = "Arial",
    font_size: int = 12,
    font_weight: str = "normal",
    font_style: str = "normal",
) -> tuple[float, float]:

    html = f"""
    <html>
    <body style="margin:0">
      <svg xmlns="http://www.w3.org/2000/svg">
        <text
            id="measure"
            x="0"
            y="{font_size}"
            font-family="{font_family}"
            font-size="{font_size}px"
            font-weight="{font_weight}"
            font-style="{font_style}">
            {text}
        </text>
      </svg>
    </body>
    </html>
    """

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html)

        width, height = page.evaluate("""
        () => {
            const text = document.getElementById('measure');
            const bbox = text.getBBox();
            return [bbox.width, bbox.height];
        }
        """)

        browser.close()

    return width, height
