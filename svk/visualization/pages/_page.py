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

from abc import ABC, abstractmethod
from pydantic import BaseModel
from svgwrite import Drawing

from svk.data import StormSurgeBarrier, LinksRegister, Translator
from svk.visualization._layout_configuration import LayoutConfiguration
from svk.visualization.helpers._draw_disclaimer import draw_disclaimer
from svk.visualization.helpers._draw_scaled_icon import draw_scaled_icon
from svk.visualization.helpers._draw_callout import draw_callout


class Page(BaseModel, ABC):
    title: str
    """The title of this page."""
    # TODO: Include the page number somewhere on the page as well?
    page_number: int
    """The page number"""
    icon: StormSurgeBarrier | None = None
    """The icon of this page."""
    title_link_target: str | None = None
    """Optional link target to the title of the page."""
    disclaimer: str | None = None
    """An optional disclaimer text, placed at the bottom of the page."""
    disclaimer_links: list[tuple[str, str]] | None = None
    """A list of strings and link replacements in the disclaimer text."""
    layout_configuration: LayoutConfiguration
    """The layout configuration shared across all elements of a document."""
    links_register: LinksRegister
    """The links register shared across all elements of a document."""
    translator: Translator
    """The translator that should be used for this page."""

    @abstractmethod
    def get_content_size(self) -> tuple[float, float]:
        pass

    @abstractmethod
    def draw_content(self, dwg: Drawing, left: float, top: float):
        pass

    def get_size(self) -> tuple[float, float]:
        content_size = self.get_content_size()
        title_height = (
            self.layout_configuration.paper_margin + self.layout_configuration.page_title_height + self.layout_configuration.large_margin
        )
        disclaimer_height = (
            (self.layout_configuration.large_margin + 1.2 * self.layout_configuration.disclamer_font_size)
            if self.disclaimer is not None
            else 0.0
        )
        page_width = content_size[0]
        page_height = title_height + content_size[1] + disclaimer_height + self.layout_configuration.paper_margin
        return (page_width, page_height)

    def draw(self) -> Drawing:
        (page_width, page_height) = self.get_size()

        dwg = Drawing(size=(f"{page_width}px", f"{page_height}px"), debug=False)
        self.links_register.register_page(self.page_number, page_width, page_height)

        self.draw_title(dwg=dwg)

        self.draw_content(
            dwg=dwg,
            left=self.layout_configuration.paper_margin,
            top=self.layout_configuration.paper_margin
            + self.layout_configuration.page_title_height
            + self.layout_configuration.large_margin,
        )

        self.draw_disclaimer(dwg=dwg)

        return dwg

    def draw_title(self, dwg: Drawing):
        left_title = self.layout_configuration.paper_margin
        if self.icon is not None:
            icon_size = self.layout_configuration.page_title_height
            icon_width = icon_size + self.layout_configuration.arrow_depth
            draw_callout(
                dwg, self.layout_configuration.paper_margin, self.layout_configuration.paper_margin, icon_width, icon_size, "#000000"
            )
            draw_scaled_icon(
                dwg=dwg,
                storm_surge_barrier=self.icon,
                insert=(
                    self.layout_configuration.paper_margin + self.layout_configuration.arrow_depth + 2,
                    self.layout_configuration.paper_margin + 2,
                ),
                size=(icon_size - 4, icon_size - 4),
            )
            left_title = 2 * self.layout_configuration.paper_margin + icon_width

        dwg.add(
            dwg.text(
                self.title,
                insert=(
                    left_title,
                    self.layout_configuration.paper_margin + self.layout_configuration.page_title_height / 2,
                ),
                font_size=self.layout_configuration.page_title_font_size,
                font_family="Arial",
                font_weight="bold",
                text_anchor="start",
                dominant_baseline="middle",
            )
        )

        if self.title_link_target is not None:
            self.links_register.register_link_target(
                self.title_link_target,
                self.page_number,
                left_title,
                self.layout_configuration.paper_margin
                + self.layout_configuration.page_title_height / 2
                - self.layout_configuration.page_title_font_size * 1.2 / 2,
            )

    def draw_disclaimer(self, dwg: Drawing):
        if self.disclaimer is not None:
            (_, page_height) = self.get_size()
            draw_disclaimer(
                dwg=dwg,
                disclaimer_text=self.disclaimer,
                insert=(
                    self.layout_configuration.paper_margin,
                    page_height - self.layout_configuration.paper_margin - self.layout_configuration.disclamer_font_size * 1.2,
                ),
                dominant_baseline="hanging",
                text_anchor="start",
                font_size=self.layout_configuration.disclamer_font_size,
                links=self.disclaimer_links if self.disclaimer_links is not None else [],
            )
