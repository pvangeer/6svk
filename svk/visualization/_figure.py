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

from svk.data import TimeFrame
from svk.visualization._column import Column

from svgwrite import Drawing


class Figure(BaseModel):
    disclaimer: str = (
        "Dit is een eerste concept van de onderzoeksagenda stormvloedkeringen. Deze versie is ontstaan in samenwerking met de asset management teams van de keringen. De prioritering van de onderzoeksvragen moet nog gereviewd worden door o.a. de asset management teams en RWS WVL/GPO. De indeling in tijdsperiode is op dit moment in ontwikkeling. Voor vragen, neem contact op met Marit de Jong of Riva de Vries."
    )
    columns: list[Column] = [Column(time_frame=TimeFrame.Now), Column(time_frame=TimeFrame.NearFuture), Column(time_frame=TimeFrame.Future)]
    paper_margin: int = 20
    disclamer_font_size: int = 8

    def draw(self) -> Drawing:
        y_start_group_1 = self.columns[0].header.height + 2 * self.paper_margin
        y_start_group_2 = y_start_group_1 + max(
            sum([g.get_height() + c.group_margin for g in c.groups if g.research_line.color_group == 1]) for c in self.columns
        )
        y_start_group_3 = y_start_group_2 + max(
            sum([g.get_height() + c.group_margin for g in c.groups if g.research_line.color_group == 2]) for c in self.columns
        )
        for column in self.columns:
            column.y_group_1 = y_start_group_1
            column.y_group_2 = y_start_group_2
            column.y_group_3 = y_start_group_3

        column_widths = [column.get_width() for column in self.columns]
        column_heights = [column.get_height() for column in self.columns]

        paper_height = self.paper_margin * 3 + max(column_heights) + 1.2 * self.disclamer_font_size
        dwg = Drawing(size=(f"{self.paper_margin * 2 + sum(column_widths)}px", f"{paper_height}px"), debug=False)

        x_current = self.paper_margin
        for column in self.columns:
            column.draw(dwg, x_current, self.paper_margin)
            x_current = x_current + column.get_width()

        parts = self.disclaimer.split("Riva de Vries")

        disclaimer_text_element = dwg.text(
            parts[0],
            insert=(self.paper_margin, self.paper_margin * 2 + max(column_heights)),
            dominant_baseline="hanging",
            text_anchor="start",
            font_size=self.disclamer_font_size,
        )

        link = dwg.a("mailto:riva.de.vries@rws.nl")

        link.add(
            dwg.tspan(
                "Riva de Vries",
                fill="blue",
                text_decoration="underline",
                cursor="pointer",
            )
        )

        disclaimer_text_element.add(link)
        disclaimer_text_element.add(dwg.tspan(parts[1], font_size=self.disclamer_font_size))

        dwg.add(disclaimer_text_element)
        return dwg
