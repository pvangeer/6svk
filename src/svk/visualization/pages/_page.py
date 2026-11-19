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
from abc import abstractmethod

from pydantic import ConfigDict, PrivateAttr
from svgwrite import Drawing
from svk.data import Icon, KnownColors, Label
from svk.visualization._visual_component import VisualComponent
from svk.visualization.elements._disclaimer_element import DisclaimerElement
from svk.visualization.elements._legend_reference_element import LegendReferenceElement
from svk.visualization.helpers._draw_disclaimer import draw_disclaimer, get_disclaimer_width
from svk.visualization.helpers._draw_scaled_icon import draw_scaled_icon
from svk.visualization.helpers._draw_callout import draw_callout
from svk.visualization.helpers._measuretext import measure_text


class Page(VisualComponent):
    model_config = ConfigDict(frozen=True)

    title: str
    """The title of this page."""
    subtitle: str | None = None
    """An optional subtitle of this page."""
    # TODO: Include the page number somewhere on the page as well?
    page_number: int
    """The page number"""
    icon: Icon | None = None
    """The icon of this page."""
    title_link_target: str | None = None
    """Optional link target to the title of the page."""
    disclaimer: str | None = None
    """An optional disclaimer text, placed at the bottom of the page."""
    disclaimer_links: list[tuple[str, str]] | None = None
    """A list of strings and link replacements in the disclaimer text."""
    include_legend_link: bool = False

    _title_width: float = 0.0
    _title_height: float = 0.0
    _legend_link_element: LegendReferenceElement | None = PrivateAttr(default=None)
    _disclaimer_element: DisclaimerElement | None = PrivateAttr(default=None)

    def measure(self) -> None:
        content_size = self.get_content_size()
        _width_legend_label = self._legend_link_element.width if self._legend_link_element is not None else 0.0
        _disclaimer_width = self._disclaimer_element.width if self._disclaimer_element is not None else 0.0

        self._width = max(
            [
                content_size[0] + 2 * self.layout_configuration.paper_margin,
                self._title_width,
                self.layout_configuration.paper_margin * 2
                + _disclaimer_width
                + ((self.layout_configuration.intermediate_margin + _width_legend_label) if self.include_legend_link else 0.0),
            ]
        )
        self._height = (
            self.layout_configuration.paper_margin
            + self._title_height
            + self.layout_configuration.large_margin
            + content_size[1]
            + self.layout_configuration.large_margin
            + max(
                self._disclaimer_element.height if self._disclaimer_element is not None else 0.0,
                self._legend_link_element.height if self._legend_link_element is not None else 0.0,
            )
            + self.layout_configuration.paper_margin
        )

    def initialize(self) -> None:
        self._title_height = (
            self.layout_configuration.page_title_font_size
            if self.subtitle is None
            else self.layout_configuration.page_title_font_size
            + self.layout_configuration.small_margin
            + self.layout_configuration.page_subtitle_font_size
        )
        _title_text_width = (
            self.layout_configuration.paper_margin
            + measure_text(
                self.title,
                font_size=self.layout_configuration.page_title_font_size,
                font_weight="bold",
                font_family=self.layout_configuration.font_family,
            )[0]
            + self.layout_configuration.paper_margin
        )
        self._title_width = (
            (self.layout_configuration.paper_margin + self.layout_configuration.arrow_depth + self._title_height + _title_text_width)
            if self.icon is not None
            else _title_text_width
        )
        self._legend_link_element = (
            self.create(LegendReferenceElement, page_number=self.page_number, color=KnownColors.GreyAccent)
            if self.include_legend_link
            else None
        )
        self._disclaimer_element = (
            self.create(DisclaimerElement, color=KnownColors.GreyAccent, disclaimer=self.disclaimer, disclaimer_links=self.disclaimer_links)
            if self.disclaimer is not None
            else None
        )

    @abstractmethod
    def get_content_size(self) -> tuple[float, float]:
        """This method calculates the width and height of the content of the page in pixels."""

    @abstractmethod
    def draw_content(self, dwg: Drawing, left: float, top: float) -> None:
        """This method takes care of drawing the content of the page."""
        pass

    def render(self) -> Drawing:
        """Renders the entire page."""

        dwg = Drawing(size=(f"{self._width}px", f"{self._height}px"), debug=False)
        self.links_register.register_page(self.page_number, self._width, self._height)

        self.draw_title(dwg=dwg)

        x_left = (self.width - self.get_content_size()[0]) / 2

        self.draw_content(
            dwg=dwg,
            left=x_left,
            top=self.layout_configuration.paper_margin + self._title_height + self.layout_configuration.large_margin,
        )

        self.draw_disclaimer(dwg=dwg)
        self.draw_legend_link(dwg=dwg)

        return dwg

    def draw_title(self, dwg: Drawing):
        left_title = self.layout_configuration.paper_margin
        if self.icon is not None:
            icon_size = self._title_height
            icon_width = icon_size + self.layout_configuration.arrow_depth
            draw_callout(
                dwg=dwg,
                x=self.layout_configuration.paper_margin,
                y=self.layout_configuration.paper_margin,
                width=icon_width,
                height=icon_size,
                use_gradients=self.layout_configuration.use_gradients,
                stroke=KnownColors.Black,
                fill=KnownColors.White,
                arrow_height=self.layout_configuration.arrow_height,
                arrow_depth=self.layout_configuration.arrow_depth,
                header_fill=KnownColors.Black,
                use_header_fill=self.layout_configuration.use_gradients,
            )
            draw_scaled_icon(
                dwg=dwg,
                icon=self.icon,
                insert=(
                    self.layout_configuration.paper_margin + self.layout_configuration.arrow_depth + 2,
                    self.layout_configuration.paper_margin + 2,
                ),
                size=(icon_size - 4, icon_size - 4),
            )
            left_title = 2 * self.layout_configuration.paper_margin + icon_width

        bottom_title = (
            self.layout_configuration.paper_margin + self._title_height
            if self.subtitle is None
            else self.layout_configuration.paper_margin
            + self._title_height
            - self.layout_configuration.page_subtitle_font_size
            - self.layout_configuration.small_margin
        )
        dwg.add(
            dwg.text(
                self.title,
                insert=(
                    left_title,
                    bottom_title,
                ),
                font_size=self.layout_configuration.page_title_font_size,
                font_family=self.layout_configuration.font_family,
                font_weight="bold",
                text_anchor="start",
                dominant_baseline="text-bottom",
            )
        )

        if self.subtitle is not None:
            dwg.add(
                dwg.text(
                    self.subtitle,
                    insert=(left_title, self.layout_configuration.paper_margin + self._title_height),
                    font_size=self.layout_configuration.page_subtitle_font_size,
                    font_family=self.layout_configuration.font_family,
                    font_weight="normal",
                    text_anchor="start",
                    dominant_baseline="text-bottom",
                )
            )

        if self.title_link_target is not None:
            self.links_register.register_link_target(
                self.title_link_target,
                self.page_number,
                left_title,
                self.layout_configuration.paper_margin,
            )

    def draw_disclaimer(self, dwg: Drawing):
        if self.disclaimer is not None and self._disclaimer_element is not None:
            self._disclaimer_element.draw(
                dwg=dwg,
                x=self.layout_configuration.paper_margin,
                y=self._height - self.layout_configuration.paper_margin - self._disclaimer_element.height,
            )

    def draw_legend_link(self, dwg: Drawing):
        if self.include_legend_link and self._legend_link_element is not None:
            x_left = self._width - self.layout_configuration.paper_margin - self._legend_link_element.width
            y_top = self._height - self.layout_configuration.paper_margin - self._legend_link_element.height

            self._legend_link_element.draw(dwg=dwg, x=x_left, y=y_top)
