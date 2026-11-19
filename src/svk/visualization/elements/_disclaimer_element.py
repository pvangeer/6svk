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

from pydantic import PrivateAttr
from svk.data import Color, KnownColors
from svk.visualization.elements._visual_element import VisualElement
from svk.visualization.helpers._draw_disclaimer import draw_disclaimer, get_disclaimer_width
from svk.visualization.helpers._draw_callout import draw_callout


class DisclaimerElement(VisualElement):
    color: Color
    disclaimer: str
    """An optional disclaimer text, placed at the bottom of the page."""
    disclaimer_links: list[tuple[str, str]] | None = None
    """A list of strings and link replacements in the disclaimer text."""

    _disclaimer_height: float = PrivateAttr(default=0.0)

    def initialize(self) -> None:
        pass

    def measure(self) -> None:
        self._disclaimer_height = (1.2 * self.layout_configuration.disclamer_font_size) if self.disclaimer is not None else 0.0
        _disclaimer_width = get_disclaimer_width(
            disclaimer_text=self.disclaimer,
            font_family=self.layout_configuration.font_family,
            font_size=self.layout_configuration.disclamer_font_size,
            links=self.disclaimer_links,
        )[0]
        self._width = self.layout_configuration.arrow_depth + _disclaimer_width + self.layout_configuration.intermediate_margin * 2
        self._height = max(self.layout_configuration.arrow_height, self._disclaimer_height + self.layout_configuration.small_margin * 2)

    def _draw(self, x: float, y: float):
        draw_callout(
            dwg=self._dwg,
            x=x,
            y=y,
            width=self._width,
            height=self._height,
            stroke=self.color,
            header_fill=self.color,
            fill=KnownColors.White,
            stroke_width=1.0,
            arrow_height=self.layout_configuration.arrow_height,
            arrow_depth=self.layout_configuration.arrow_depth,
            use_gradients=self.layout_configuration.use_gradients,
        )

        x_start_text = x + self.layout_configuration.arrow_depth + self.layout_configuration.intermediate_margin
        y_top_text = y + self.height / 2 - self._disclaimer_height / 2
        draw_disclaimer(
            dwg=self._dwg,
            disclaimer_text=self.disclaimer,
            insert=(
                x_start_text,
                y_top_text,
            ),
            dominant_baseline="hanging",
            text_anchor="start",
            font_family=self.layout_configuration.font_family,
            font_size=self.layout_configuration.disclamer_font_size,
            links=self.disclaimer_links if self.disclaimer_links is not None else [],
        )
