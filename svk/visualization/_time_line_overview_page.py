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
from svk.visualization._page import Page
from svgwrite import Drawing


class TimeLineOverviewPage(Page):
    """
    The overview page of the "kennisagenda"
    """

    columns: list[Column] = []
    """The columns included in this overview page (that all hold groups and questions)"""
    clusters: list[Cluster] = []

    def get_content_size(self) -> tuple[float, float]:
        self.layout_configuration.n_columns = len(self.columns)
        max_column_height = sum([c.get_height() for c in self.clusters]) + self.layout_configuration.large_margin * (len(self.clusters) - 1)

        return (
            self.layout_configuration.overview_page_width,
            self.layout_configuration.column_header_height + self.layout_configuration.large_margin + max_column_height,
        )

    def draw_content(self, dwg: Drawing, left: float, top: float):
        left_current = left
        for column in sorted(self.columns, key=lambda c: c.number):
            column.draw(dwg, left_current, top)
            left_current += self.layout_configuration.column_width

        top_current = top + self.layout_configuration.column_header_height + self.layout_configuration.large_margin
        for cluster in self.clusters:
            cluster.draw(dwg=dwg, left=self.layout_configuration.paper_margin, top=top_current)
            top_current += cluster.get_height() + self.layout_configuration.large_margin
