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
from pydantic import BaseModel
from svk.visualization.helpers._drawchevron import draw_half_chevron


class Header(BaseModel):
    title: str
    sub_title: str
    height: int = 60
    width: int = 650
    arrow_depth: int = 20
    text_margin: int = 10
    font_size: int = 18
    color: str

    def draw(self, dwg: Drawing, x: int, y: int):
        dwg.add(draw_half_chevron(dwg, x=x, y=y, width=self.width, height=self.height, color=self.color))
        y_column_header_text = y + self.height / 2
        dwg.add(
            dwg.text(
                self.title,
                insert=(x + self.arrow_depth + self.text_margin, y_column_header_text),
                font_size=self.font_size,
                font_family="Arial",
                font_weight="bold",
                text_anchor="start",
                dominant_baseline="middle",
            )
        )
        if self.sub_title != "":
            dwg.add(
                dwg.text(
                    self.sub_title,
                    insert=(x + self.width - self.arrow_depth, y_column_header_text),
                    font_family="Arial",
                    text_anchor="end",
                    dominant_baseline="middle",
                    font_size=self.font_size,
                    font_weight="normal",
                )
            )
