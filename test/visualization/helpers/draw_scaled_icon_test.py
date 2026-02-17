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

from svgwrite import Drawing
from svk.data import StormSurgeBarrier
from svk.visualization.helpers import draw_scaled_icon
from svk.io import svg_to_pdf_chrome


def test_draw_icon():
    dwg = Drawing(size=("100px", "100px"))
    draw_scaled_icon(dwg, storm_surge_barrier=StormSurgeBarrier.MaeslantBarrier, insert=(5, 10), size=(12, 12))
    draw_scaled_icon(dwg, storm_surge_barrier=StormSurgeBarrier.HaringvlietBarrier, insert=(25, 15), size=(24, 24))
    draw_scaled_icon(dwg, storm_surge_barrier=StormSurgeBarrier.Ramspol, insert=(80, 30), size=(16, 16))
    draw_scaled_icon(dwg, storm_surge_barrier=StormSurgeBarrier.HartelBarrier, insert=(10, 70), size=(35, 35))
    draw_scaled_icon(dwg, storm_surge_barrier=StormSurgeBarrier.EasternScheldBarrier, insert=(40, 60), size=(24, 24))
    draw_scaled_icon(dwg, storm_surge_barrier=StormSurgeBarrier.HollandseIJsselBarrier, insert=(80, 80), size=(16, 16))
    svg_to_pdf_chrome(dwg, "C:/Test/icon.pdf")
