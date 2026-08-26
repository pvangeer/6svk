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

from playwright.sync_api import sync_playwright, Page, Browser, Playwright
from svgwrite import Drawing
from html import escape
from pathlib import Path


class RendererNotStartedError(Exception):
    """Raised when the RendererServer was not started correctly."""

    pass


class RendererServer:
    _playwright: Playwright | None = None
    _browser: Browser | None = None
    _page: Page | None = None
    _measure_page: Page | None = None

    @classmethod
    def start(cls):
        if cls._browser is None:
            cls._playwright = sync_playwright().start()
            cls._browser = cls._playwright.chromium.launch(headless=True)

        if cls._page is None or cls._page.is_closed():
            cls._page = cls._browser.new_page()
        if cls._measure_page is None or cls._measure_page.is_closed():
            cls._measure_page = cls._browser.new_page()
            cls._measure_page.set_content("""
                <html>
                <body>
                <svg xmlns="http://www.w3.org/2000/svg">
                    <text id="measure"></text>
                </svg>
                </body>
                </html>
                """)

    @classmethod
    def svg_to_pdf(cls, dwg: Drawing, path: Path):
        """
        Save an svgwrite.Drawing object to PDF with all effects and links preserved.

        Parameters:
        -----------
        svg_dwg : svgwrite.Drawing
            The svgwrite SVG object to export.
        pdf_path : str
            Path to the output PDF file.
        """

        cls.start()
        if cls._page is None:
            raise RendererNotStartedError()

        svg_content = dwg.tostring()

        html = f"""
        <html>
        <body style="margin:0; padding:0;">
            {svg_content}
        </body>
        </html>
        """
        cls._page.set_content(html)

        width = str(dwg.attribs.get("width")) if "width" in dwg.attribs else "800px"
        height = str(dwg.attribs.get("height")) if "height" in dwg.attribs else "600px"

        cls._page.pdf(path=path, width=width, height=height, print_background=True)

    @classmethod
    def measure_text(
        cls,
        text: str,
        font_family: str = "Arial",
        font_size: int = 12,
        font_weight: str = "normal",
        font_style: str = "normal",
    ) -> tuple[float, float]:

        cls.start()
        if cls._measure_page is None:
            raise RendererNotStartedError()

        width, height = cls._measure_page.evaluate(
            """
            ([text, family, size, weight, style]) => {
                const el = document.getElementById("measure");

                el.textContent = text;
                el.setAttribute("font-family", family);
                el.setAttribute("font-size", size + "px");
                el.setAttribute("font-weight", weight);
                el.setAttribute("font-style", style);

                const bbox = el.getBBox();
                return [bbox.width, bbox.height];
            }
            """,
            [escape(text), font_family, font_size, font_weight, font_style],
        )

        return width, height

    @classmethod
    def stop(cls):
        if cls._page:
            cls._page.close()
            cls._page = None

        if cls._browser:
            cls._browser.close()
            cls._browser = None

        if cls._playwright:
            cls._playwright.stop()
            cls._playwright = None


def svg_to_pdf(svg_dwg: Drawing, path: Path):
    """
    Save an svgwrite.Drawing object to PDF with all effects and links preserved.

    Parameters:
    -----------
    svg_dwg : svgwrite.Drawing
        The svgwrite SVG object to export.
    pdf_path : str
        Path to the output PDF file.
    """
    RendererServer.svg_to_pdf(svg_dwg, path)
