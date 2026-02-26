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

from svk.visualization._column import Column
from svk.visualization._cluster import Cluster
from svk.data import StormSurgeBarrier
from svk.visualization.helpers._draw_disclaimer import draw_disclaimer
from svk.visualization.helpers._draw_scaled_icon import draw_scaled_icon
from svk.visualization.helpers._draw_callout import draw_callout
from svk.visualization._visual_element import VisualElement
from svgwrite import Drawing
from uuid import uuid4


class OverviewPage(VisualElement):
    """
    The overview page of the "kennisagenda"
    """

    storm_surge_barrier: StormSurgeBarrier
    """The storm surge barrier associated to this overview page (used for including an icon in the header)"""
    page_number: int
    title: str
    """The title of the overview page"""
    disclaimer: str = (
        "Dit is een eerste concept van de onderzoeksagenda stormvloedkeringen. Deze versie is ontstaan in samenwerking met de asset management teams van de keringen. De prioritering van de onderzoeksvragen moet nog gereviewd worden door o.a. de asset management teams en RWS WVL/GPO. De indeling in tijdsperiode is op dit moment in ontwikkeling. Voor vragen, neem contact op met Marit de Jong of Riva de Vries."
    )
    """A disclaimer text (printed at the bottom)"""
    columns: list[Column] = []
    """The columns included in this overview page (that all hold groups and questions)"""

    clusters: list[Cluster] = []

    def draw(self) -> Drawing:
        self.layout_configuration.n_columns = len(self.columns)

        y_column_header = (
            self.layout_configuration.paper_margin + self.layout_configuration.page_title_height + self.layout_configuration.large_margin
        )

        y_top_questions = y_column_header + self.layout_configuration.column_header_height + self.layout_configuration.large_margin

        y_current = y_top_questions
        for cluster in self.clusters:
            cluster.y_top = y_current
            y_current += cluster.get_height() + self.layout_configuration.large_margin

        max_column_height = self._get_max_column_height()

        paper_height = (
            self.layout_configuration.paper_margin
            + self.layout_configuration.page_title_height
            + self.layout_configuration.large_margin
            + self.layout_configuration.column_header_height
            + self.layout_configuration.large_margin
            + max_column_height
            + self.layout_configuration.large_margin
            + 1.2 * self.layout_configuration.disclamer_font_size
            + self.layout_configuration.paper_margin
        )

        dwg = Drawing(size=(f"{self.layout_configuration.overview_page_width}px", f"{paper_height}px"), debug=False)
        self.links_register.register_page(self.page_number, self.layout_configuration.overview_page_width, paper_height)

        self.draw_title(dwg=dwg)

        x_current = self.layout_configuration.paper_margin
        for column in sorted(self.columns, key=lambda c: c.number):
            column.draw(dwg, x_current, y_column_header)
            x_current += self.layout_configuration.column_width

        y_current = y_top_questions
        for cluster in self.clusters:
            cluster.draw(dwg=dwg)
            y_top_questions += cluster.get_height(column) + self.layout_configuration.intermediate_margin

        draw_disclaimer(
            dwg=dwg,
            disclaimer_text=self.disclaimer,
            insert=(
                self.layout_configuration.paper_margin,
                self.layout_configuration.paper_margin
                + self.layout_configuration.page_title_height
                + self.layout_configuration.large_margin
                + self.layout_configuration.column_header_height
                + self.layout_configuration.large_margin
                + max_column_height
                + self.layout_configuration.large_margin,
            ),
            dominant_baseline="hanging",
            text_anchor="start",
            font_size=self.layout_configuration.disclamer_font_size,
            links=[("Riva de Vries", "mailto:riva.de.vries@rws.nl"), ("Marit de Jong", "mailto:marit.de.jong@rws.nl")],
        )

        return dwg

    def draw_title(self, dwg):
        icon_size = self.layout_configuration.page_title_height
        icon_width = icon_size + self.layout_configuration.arrow_depth
        draw_callout(dwg, self.layout_configuration.paper_margin, self.layout_configuration.paper_margin, icon_width, icon_size, "#000000")
        draw_scaled_icon(
            dwg=dwg,
            storm_surge_barrier=self.storm_surge_barrier,
            insert=(
                self.layout_configuration.paper_margin + self.layout_configuration.arrow_depth + 2,
                self.layout_configuration.paper_margin + 2,
            ),
            size=(icon_size - 4, icon_size - 4),
        )

        dwg.add(
            dwg.text(
                self.title,
                insert=(
                    2 * self.layout_configuration.paper_margin + icon_width,
                    self.layout_configuration.paper_margin + self.layout_configuration.page_title_height / 2,
                ),
                font_size=self.layout_configuration.page_title_font_size,
                font_family="Arial",
                font_weight="bold",
                text_anchor="start",
                dominant_baseline="middle",
            )
        )

    def _get_max_column_height(self):
        return sum([c.get_height() for c in self.clusters]) + self.layout_configuration.large_margin * (len(self.clusters) - 1)
