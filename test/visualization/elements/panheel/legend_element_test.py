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

from svk.visualization import LayoutConfiguration, LegendPage
from svk.data import LinksRegister, Translator
from svk.io import svg_to_pdf
from test.paths import test_output_dir


def test_draw_legend_page():

    page = LegendPage(
        layout_configuration=LayoutConfiguration(use_rijkswaterstaat_colors=True),
        links_register=LinksRegister(),
        translator=Translator(),
        title="Legend Page",
        subtitle="Test Subtitle",
        page_number=1,
    )

    svg_to_pdf(svg_dwg=page.draw(), path=test_output_dir / "test_legend_page.pdf")
