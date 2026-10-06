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
import math
from pydantic import PrivateAttr, model_validator
from svgwrite import Drawing
from svk.data import Color, KnownColors
from svk.visualization.elements._visual_element import VisualElement
from svk.visualization.helpers._measuretext import measure_text


class CodeExplanationLegendElement(VisualElement):
    color: Color
    """The color of the group"""

    _width: float = PrivateAttr()
    _height: float = PrivateAttr()
    _tw_code_text: float = PrivateAttr()
    _tw_sp_explanation: float = PrivateAttr()
    _tw_number_explanation: float = PrivateAttr()
    _tw_codes_explained: float = PrivateAttr()

    _sp_code_color: Color = KnownColors.RWSBlue2
    _number_color: Color = KnownColors.RWSGrey1
    _code_color: Color = KnownColors.RWSYellow2
    _code_explanations: tuple[tuple[str, str], ...] = (
        ("C", "Vraag afkomstig uit inventarisatie componenten."),
        ("ET", "Vraag afkomstig uit einde technische levensduur analyse."),
        ("EF", "Vraag afkomstig uit einde functionele levensduur analyse."),
        ("A", "Algemeen geldende kennisvraag."),
    )
    _code_explanation_indent: float = 20
    _line_height_factor: float = 1.6
    _sp_explanation: str = "Vraag gesteld bij sessie met Sluizencomplex Panheel"
    _number_explanation: str = "Volgnummer"

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    @model_validator(mode="after")
    def validate(self) -> CodeExplanationLegendElement:
        self._tw_code_text = self.text_width("SP_XX##")
        self._tw_sp_explanation = self.text_width(self._sp_explanation)
        self._tw_number_explanation = self.text_width(self._number_explanation)
        self._tw_codes_explained = max([measure_text(l, self.layout_configuration.font_size)[0] for _, l in self._code_explanations])

        self._width = max([self._code_explanation_indent + self._tw_codes_explained, self._tw_sp_explanation])
        self._height = 8 * self.layout_configuration.font_size * self._line_height_factor + self.layout_configuration.font_size
        return self

    def draw(self, dwg: Drawing, x: float, y: float):
        lh = self.layout_configuration.font_size * self._line_height_factor
        font_size = self.layout_configuration.font_size

        # Top text
        dwg.add(
            dwg.text(
                self._sp_explanation,
                insert=(x, y),
                font_size=font_size,
                font_family=self.layout_configuration.font_family,
                text_anchor="start",
                dominant_baseline="hanging",
            )
        )

        # Right label
        x_number_text = x + 0.6 * self.width
        y_number_text = y + lh
        dwg.add(
            dwg.text(
                self._number_explanation,
                insert=(x_number_text, y_number_text),
                font_size=font_size,
                font_family=self.layout_configuration.font_family,
                text_anchor="start",
                dominant_baseline="hanging",
            )
        )

        x_center = x + 0.5 * self.width
        y_center_text = y + 3 * lh
        # Central code
        text = dwg.text(
            "",
            insert=(x_center, y_center_text),
            font_size=font_size,
            font_family=self.layout_configuration.font_family,
            text_anchor="middle",
            dominant_baseline="hanging",
        )

        text.add(dwg.tspan("SP", fill=self._sp_code_color))
        text.add(dwg.tspan("_", fill=KnownColors.Black))
        text.add(dwg.tspan("XX", fill=self._code_color))
        text.add(dwg.tspan("##", fill=self._number_color))

        dwg.add(text)

        m = 0.2 * lh
        # Left arrow
        draw_arrow(
            dwg,
            start=(x_center - self._tw_code_text * 0.3, y_center_text - m),
            end=(x + self.width * 0.2, y + lh),
            color=str(self._sp_code_color),
        )

        # Right arrow
        draw_arrow(
            dwg,
            start=(x_center + self._tw_code_text * 0.4, y_center_text - m),
            end=(x_number_text + 0.5 * self._tw_number_explanation, y_number_text + lh),
            color=str(self._number_color),
        )

        # Downward arrow
        draw_arrow(
            dwg,
            start=(x_center + 0.1 * self._tw_code_text, y_center_text + lh),
            end=(x_center + 0.1 * self._tw_code_text, y_center_text + 2 * lh - m),
            color=str(self._code_color),
        )

        # Description lines
        explanations = [
            ("C", "Vraag afkomstig uit inventarisatie componenten."),
            ("ET", "Vraag afkomstig uit einde technische levensduur analyse."),
            ("EF", "Vraag afkomstig uit einde functionele levensduur analyse."),
            ("A", "Algemeen geldende kennisvraag."),
        ]

        y = y_center_text + 2 * lh
        x_explained_left = x
        for code, text in explanations:
            dwg.add(
                dwg.text(
                    code,
                    insert=(x_explained_left, y),
                    font_size=font_size,
                    font_family=self.layout_configuration.font_family,
                    font_weight="bold",
                    text_anchor="start",
                    dominant_baseline="hanging",
                )
            )
            dwg.add(
                dwg.text(
                    text,
                    insert=(x_explained_left + self._code_explanation_indent, y),
                    font_size=font_size,
                    font_family=self.layout_configuration.font_family,
                    text_anchor="start",
                    dominant_baseline="hanging",
                )
            )
            y += lh

    def text_width(self, text: str) -> float:
        return measure_text(text, self.layout_configuration.font_size)[0]


def draw_arrow(
    dwg,
    start: tuple[float, float],
    end: tuple[float, float],
    color: str,
    stroke_width: float = 2,
    head_length: float = 8,
    head_angle_deg: float = 30,
) -> None:
    x1, y1 = start
    x2, y2 = end

    # Direction of shaft
    angle = math.atan2(y2 - y1, x2 - x1)

    # Arrowhead angles
    head_angle = math.radians(head_angle_deg)

    left_angle = angle + math.pi - head_angle
    right_angle = angle + math.pi + head_angle

    # Arrowhead points
    lx = x2 + head_length * math.cos(left_angle)
    ly = y2 + head_length * math.sin(left_angle)

    rx = x2 + head_length * math.cos(right_angle)
    ry = y2 + head_length * math.sin(right_angle)

    # Shaft
    dwg.add(
        dwg.line(
            start=(x1, y1),
            end=(x2, y2),
            stroke=color,
            stroke_width=stroke_width,
            stroke_linecap="round",
        )
    )

    # Left side of head
    dwg.add(
        dwg.line(
            start=(x2, y2),
            end=(lx, ly),
            stroke=color,
            stroke_width=stroke_width,
            stroke_linecap="round",
        )
    )

    # Right side of head
    dwg.add(
        dwg.line(
            start=(x2, y2),
            end=(rx, ry),
            stroke=color,
            stroke_width=stroke_width,
            stroke_linecap="round",
        )
    )
