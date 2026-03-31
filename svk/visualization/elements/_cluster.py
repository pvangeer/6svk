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

from svk.visualization.elements._visual_element import VisualElement
from svk.visualization.elements._group import GroupBase
from svk.visualization.elements._column import Column
from svk.visualization.helpers._greyfraction import color_toward_grey

from svgwrite import Drawing
from uuid import uuid4
from collections import defaultdict


class Cluster(VisualElement):
    color: tuple[int, int, int]
    """Base color of the cluster (background)"""
    groups: defaultdict[int, list[GroupBase]] = defaultdict(list[GroupBase])
    """A list of groups per column index (zero based)."""

    @property
    def width(self) -> float:
        return self.layout_configuration.overview_page_width - 2 * self.layout_configuration.paper_margin

    @property
    def height(self) -> float:
        return self.get_height()

    def get_height(self, column: Column | None = None):
        if column is None:
            return max([self._get_height_for_column(c) for c in self.groups])
        else:
            return self._get_height_for_column(column.number) if column.number in self.groups else 0.0

    def draw(self, dwg: Drawing, left: float, top: float):
        width = self.width
        height = self.height

        gradient_id = f"gradient_{str(uuid4())}"
        x_scale = width / height
        gradient_center = ((left + width / 2) / x_scale, top)
        radius = height * 1.2
        fill_radial_grad = dwg.radialGradient(
            center=gradient_center,
            r=radius,
            gradientUnits="userSpaceOnUse",
            id=gradient_id,
        )
        fill_radial_grad.add_stop_color(0, "white")
        fill_radial_grad.add_stop_color(0.6, "white")
        fill_radial_grad.add_stop_color(1, color_toward_grey(self.color, 0.5, grey=(250, 250, 250)))
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
        stroke_radial_grad.add_stop_color(1, color_toward_grey(self.color, 0.0))
        stroke_radial_grad["gradientTransform"] = f"scale({x_scale},1)"

        dwg.defs.add(fill_radial_grad)
        dwg.defs.add(stroke_radial_grad)

        dwg.add(
            dwg.rect(
                insert=(
                    left,
                    top,
                ),
                size=(width, height),
                fill=f"url(#{gradient_id})",
                stroke="none",
            )
        )
        dwg.add(
            dwg.rect(
                insert=(
                    left,
                    top,
                ),
                size=(width, height),
                fill="none",
                stroke=f"url(#{stroke_gradient_id})",
                stroke_widht=3,
            )
        )

        for i_column in self.groups:
            y_current = top
            for group in self.groups[i_column]:
                group.draw(
                    dwg=dwg, x=self.layout_configuration.paper_margin + i_column * self.layout_configuration.column_width, y=y_current
                )
                y_current += group.height + self.layout_configuration.intermediate_margin

    def _get_height_for_column(self, i_column: int):
        return (
            sum([g.height + self.layout_configuration.intermediate_margin for g in self.groups[i_column]])
            + self.layout_configuration.intermediate_margin
            - self.layout_configuration.small_margin
        )
