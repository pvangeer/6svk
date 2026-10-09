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

from __future__ import annotations
from pydantic import BaseModel, ConfigDict, model_validator, PrivateAttr
from svk.visualization.elements._visual_element import VisualElement
from svk.visualization.elements._group import GroupBase
from svk.data.helpers import color_toward_grey

from svgwrite import Drawing
from uuid import uuid4
from svk.data import Color


class ClusterColumn(BaseModel):
    model_config = ConfigDict(frozen=True)
    column_number: int
    groups: tuple[GroupBase, ...]


class Cluster(VisualElement):
    model_config = ConfigDict(frozen=True)
    color: Color
    """Base color of the cluster (background)"""
    columns: tuple[ClusterColumn, ...]
    """A list of ClusterColumns"""

    _width: float = PrivateAttr()
    _height: float = PrivateAttr()

    @model_validator(mode="after")
    def validate(self) -> Cluster:
        self._width = self.layout_configuration.overview_page_width - 2 * self.layout_configuration.paper_margin
        self._height = max([self._get_height_for_column(c) for c in self.columns])
        return self

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    def draw(self, dwg: Drawing, left: float, top: float):
        width = self.width
        height = self.height

        x_scale = width / height
        gradient_center = ((left + width / 2) / x_scale, top)
        radius = height * 1.2

        if self.layout_configuration.use_gradients:
            gradient_id = f"gradient_{str(uuid4())}"
            fill_radial_grad = dwg.radialGradient(
                center=gradient_center,
                r=radius,
                gradientUnits="userSpaceOnUse",
                id=gradient_id,
            )
            fill_radial_grad.add_stop_color(0, "white")
            fill_radial_grad.add_stop_color(0.6, "white")
            fill_radial_grad.add_stop_color(1, color_toward_grey(self.color, 0.5, grey=Color(r=250, g=250, b=250)))
            fill_radial_grad["gradientTransform"] = f"scale({x_scale},1)"
            dwg.defs.add(fill_radial_grad)

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

            dwg.defs.add(stroke_radial_grad)

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

        for groups_column in self.columns:
            y_current = top
            for group in groups_column.groups:
                group.draw(
                    dwg=dwg,
                    x=self.layout_configuration.paper_margin + groups_column.column_number * self.layout_configuration.column_width,
                    y=y_current,
                )
                y_current += group.height + self.layout_configuration.intermediate_margin

    def _get_height_for_column(self, groups_column: ClusterColumn):
        return (
            sum([g.height + self.layout_configuration.intermediate_margin for g in groups_column.groups])
            + self.layout_configuration.intermediate_margin
            - self.layout_configuration.small_margin
        )
