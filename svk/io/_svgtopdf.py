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

from playwright.sync_api import sync_playwright
from svgwrite import Drawing


def svg_to_pdf(svg_dwg: Drawing, pdf_path: str):
    """
    Save an svgwrite.Drawing object to PDF with all effects and links preserved.

    Parameters:
    -----------
    svg_dwg : svgwrite.Drawing
        The svgwrite SVG object to export.
    pdf_path : str
        Path to the output PDF file.
    """
    svg_content = svg_dwg.tostring()

    html = f"""
    <html>
      <body style="margin:0; padding:0;">
        {svg_content}
      </body>
    </html>
    """

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.set_content(html)

        width = str(svg_dwg.attribs.get("width")) if "width" in svg_dwg.attribs else "800px"
        height = str(svg_dwg.attribs.get("height")) if "height" in svg_dwg.attribs else "600px"

        page.pdf(path=pdf_path, width=width, height=height, print_background=True)

        browser.close()
