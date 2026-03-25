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

from uuid import uuid4
from svgwrite import Drawing


def create_radial_gradient(dwg: Drawing, x: float, y: float, width: float, height: float, color: str) -> str:
    gradient_id = f"gradient_group_header_{str(uuid4())}"
    x_scale = width / (height)
    radial_grad = dwg.radialGradient(
        center=(
            x / x_scale,
            y,
        ),
        r=height / 2,
        gradientUnits="userSpaceOnUse",
        id=gradient_id,
    )
    radial_grad.add_stop_color(0, color)  # center
    radial_grad.add_stop_color(1, "white")  # edge

    radial_grad["gradientTransform"] = f"scale({x_scale},1)"

    dwg.defs.add(radial_grad)

    return gradient_id
