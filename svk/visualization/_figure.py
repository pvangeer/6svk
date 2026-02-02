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
from svk.data import StormSurgeBarrier
from svk.visualization.helpers._draw_disclaimer import draw_disclaimer
from svk.visualization.helpers._draw_scaled_icon import draw_scaled_icon
from svk.visualization.helpers._draw_callout import draw_callout
from svk.visualization.helpers._greyfraction import color_toward_grey
from svgwrite import Drawing
from uuid import uuid4


class Figure(BaseModel):
    storm_surge_barrier: StormSurgeBarrier
    title: str
    title_height: int = 80
    title_font_size: int = 64
    disclaimer: str = (
        "Dit is een eerste concept van de onderzoeksagenda stormvloedkeringen. Deze versie is ontstaan in samenwerking met de asset management teams van de keringen. De prioritering van de onderzoeksvragen moet nog gereviewd worden door o.a. de asset management teams en RWS WVL/GPO. De indeling in tijdsperiode is op dit moment in ontwikkeling. Voor vragen, neem contact op met Marit de Jong of Riva de Vries."
    )
    columns: list[Column] = []
    group_colors: dict[int, tuple[int, int, int]] = {}
    paper_margin: int = 20
    disclamer_font_size: int = 8
    arrow_depth: float = 20
    group_margin: float = 10

    def draw(self) -> Drawing:
        groups = {}
        sorted_group_numbers = {key for col in self.columns for key in col.groups}
        y_current = self.columns[0].header.height + 3 * self.paper_margin + self.title_height
        for number in sorted_group_numbers:
            group_height = max(c.groups[number].get_height() + c.group_margin if number in c.groups else 0.0 for c in self.columns)
            for column in self.columns:
                column.y_groups[number] = y_current
            groups[number] = (
                y_current,
                group_height - self.group_margin,
            )  # TODO: 10 = Half the group margin, stored inside Column. Maybe make these parameters static?
            y_current = y_current + group_height + self.group_margin

        y_column_start = self.title_height + 2 * self.paper_margin
        column_widths = [column.get_width() for column in self.columns]
        column_heights = [column.get_height(y_column_start) for column in self.columns]

        paper_height = self.title_height + self.paper_margin * 4 + max(column_heights) + 1.2 * self.disclamer_font_size
        paper_width = self.paper_margin * 2 + sum(column_widths)

        dwg = Drawing(size=(f"{paper_width}px", f"{paper_height}px"), debug=False)

        icon_width = 0
        icon_size = self.title_height
        icon_width = icon_size + self.arrow_depth
        draw_callout(dwg, self.paper_margin, self.paper_margin, icon_width, icon_size, "#000000")
        draw_scaled_icon(
            dwg=dwg,
            storm_surge_barrier=self.storm_surge_barrier,
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

        for number in groups.keys():
            x_group = self.paper_margin
            y_group = groups[number][0]
            group_width = paper_width - 2 * self.paper_margin
            group_height = groups[number][1]
            group_color = self.group_colors[number] if number in self.group_colors else None
            if group_color is None:
                continue

            gradient_id = f"gradient_{str(uuid4())}"
            x_scale = group_width / group_height
            gradient_center = ((x_group + group_width / 2) / x_scale, y_group)
            radius = group_height * 1.2
            fill_radial_grad = dwg.radialGradient(
                center=gradient_center,
                r=radius,
                gradientUnits="userSpaceOnUse",
                id=gradient_id,
            )
            fill_radial_grad.add_stop_color(0, "white")
            fill_radial_grad.add_stop_color(0.6, "white")
            fill_radial_grad.add_stop_color(1, color_toward_grey(group_color, 0.5, grey=(250, 250, 250)))
            fill_radial_grad["gradientTransform"] = f"scale({x_scale},1)"

            stroke_gradient_id = f"gradient_{str(uuid4())}"
            stroke_radial_grad = dwg.radialGradient(
                center=gradient_center,
                r=radius,
                gradientUnits="userSpaceOnUse",
                id=stroke_gradient_id,
            )
            stroke_radial_grad.add_stop_color(0, "white")
            stroke_radial_grad.add_stop_color(0.6, "white")
            stroke_radial_grad.add_stop_color(1, color_toward_grey(group_color, 0.0))
            stroke_radial_grad["gradientTransform"] = f"scale({x_scale},1)"

            dwg.defs.add(fill_radial_grad)
            dwg.defs.add(stroke_radial_grad)

            dwg.add(
                dwg.rect(
                    insert=(
                        x_group,
                        y_group,
                    ),
                    size=(group_width, group_height),
                    fill=f"url(#{gradient_id})",
                    stroke="none",
                )
            )
            dwg.add(
                dwg.rect(
                    insert=(
                        x_group,
                        y_group,
                    ),
                    size=(group_width, group_height),
                    fill="none",
                    stroke=f"url(#{stroke_gradient_id})",
                    stroke_widht=3,
                )
            )

        x_current = self.paper_margin
        for column in self.columns:
            column.draw(dwg, x_current, y_column_start)
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
