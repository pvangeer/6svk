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

from pydantic import BaseModel
from svk.visualization._column import Column
from svk.visualization.helpers._draw_disclaimer import draw_disclaimer
from svk.visualization.helpers.icons._icons import BarrierIcons
from svk.visualization.helpers._draw_scaled_icon import draw_scaled_icon
from svk.visualization.helpers._draw_callout import draw_callout
from svgwrite import Drawing
import uuid
import os
import base64
from PIL import Image


class Figure(BaseModel):
    barrier_icon: BarrierIcons | None = None
    title: str
    title_height: int = 80
    title_font_size: int = 64
    disclaimer: str = (
        "Dit is een eerste concept van de onderzoeksagenda stormvloedkeringen. Deze versie is ontstaan in samenwerking met de asset management teams van de keringen. De prioritering van de onderzoeksvragen moet nog gereviewd worden door o.a. de asset management teams en RWS WVL/GPO. De indeling in tijdsperiode is op dit moment in ontwikkeling. Voor vragen, neem contact op met Marit de Jong of Riva de Vries."
    )
    columns: list[Column] = []
    paper_margin: int = 20
    disclamer_font_size: int = 8
    arrow_depth: float = 20

    def draw(self) -> Drawing:
        # TODO: Make number of groups configurable (provide list for example)
        y_start_group_1 = self.columns[0].header.height + 3 * self.paper_margin + self.title_height
        y_start_group_2 = y_start_group_1 + max(
            sum([g.get_height() + c.group_margin for g in c.groups if g.number == 1]) for c in self.columns
        )
        y_start_group_3 = y_start_group_2 + max(
            sum([g.get_height() + c.group_margin for g in c.groups if g.number == 2]) for c in self.columns
        )
        for column in self.columns:
            column.y_group_1 = y_start_group_1
            column.y_group_2 = y_start_group_2
            column.y_group_3 = y_start_group_3

        column_widths = [column.get_width() for column in self.columns]
        column_heights = [column.get_height() for column in self.columns]

        paper_height = self.title_height + self.paper_margin * 4 + max(column_heights) + 1.2 * self.disclamer_font_size
        paper_width = self.paper_margin * 2 + sum(column_widths)

        dwg = Drawing(size=(f"{paper_width}px", f"{paper_height}px"), debug=False)

        icon_width = 0
        if self.barrier_icon is not None:
            icon_size = self.title_height
            icon_width = icon_size + self.arrow_depth
            draw_callout(dwg, self.paper_margin, self.paper_margin, icon_width, icon_size, "#000000")
            draw_scaled_icon(
                dwg=dwg,
                icon=self.barrier_icon,
                insert=(self.paper_margin + self.arrow_depth + 2, self.paper_margin + 2),
                size=(icon_size - 4, icon_size - 4),
            )

        dwg.add(
            dwg.text(
                self.title,
                insert=(2 * self.paper_margin + icon_width, self.paper_margin + self.title_height / 2),
                font_size=self.title_font_size,
                font_family="Arial",
                font_weight="bold",
                text_anchor="start",
                dominant_baseline="middle",
            )
        )

        x_current = self.paper_margin
        for column in self.columns:
            column.draw(dwg, x_current, self.title_height + 2 * self.paper_margin)
            x_current = x_current + column.get_width()

        draw_disclaimer(
            dwg=dwg,
            disclaimer_text=self.disclaimer,
            insert=(self.paper_margin, self.paper_margin * 3 + max(column_heights) + self.title_height),
            dominant_baseline="hanging",
            text_anchor="start",
            font_size=self.disclamer_font_size,
            links=[("Riva de Vries", "mailto:riva.de.vries@rws.nl"), ("Marit de Jong", "mailto:marit.de.jong@rws.nl")],
        )

        return dwg
