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

from svgwrite import Drawing
from svk.io import svg_to_pdf_chrome
from svk.visualization.helpers import draw_half_chevron
import os


def test_svgtopdf_produces_figure():
    dwg = Drawing(size=("1240px", "800px"))
    dwg.add(draw_half_chevron(dwg, x=20, y=20, width=400, height=80))
    dwg.add(draw_half_chevron(dwg, x=420, y=20, width=400, height=80))
    dwg.add(draw_half_chevron(dwg, x=820, y=20, width=400, height=80))
    pt = "C:/test/testimage.pdf"
    if os.path.isfile(pt):
        os.remove(pt)

    svg_to_pdf_chrome(dwg, pt)
    assert os.path.isfile(pt)

    os.remove(pt)
