from svk.visualization._visual_element import VisualElement
from svk.visualization._group import GroupBase
from svk.visualization._column import Column
from svk.visualization.helpers._greyfraction import color_toward_grey

from svgwrite import Drawing
from uuid import uuid4
from collections import defaultdict


class Cluster(VisualElement):
    color: tuple[int, int, int]
    """Base color of the cluster (background)"""
    groups: defaultdict[int, list[GroupBase]] = defaultdict(list[GroupBase])
    """A list of groups per column index (zero based)."""
    y_top: float | None = None
    """y-coordinate of the top left of the cluster"""

    def get_height(self, column: Column | None = None):
        if column is None:
            return max([self._get_height_for_column(c) for c in self.groups])
        else:
            return self._get_height_for_column(column.number) if column.number in self.groups else 0.0

    def draw(self, dwg: Drawing):
        x_cluster = self.layout_configuration.paper_margin
        y_cluster = self.y_top
        width = self.layout_configuration.overview_page_width - 2 * self.layout_configuration.paper_margin
        height = self.get_height()

        gradient_id = f"gradient_{str(uuid4())}"
        x_scale = width / height
        gradient_center = ((x_cluster + width / 2) / x_scale, y_cluster)
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
                    x_cluster,
                    y_cluster,
                ),
                size=(width, height),
                fill=f"url(#{gradient_id})",
                stroke="none",
            )
        )
        dwg.add(
            dwg.rect(
                insert=(
                    x_cluster,
                    y_cluster,
                ),
                size=(width, height),
                fill="none",
                stroke=f"url(#{stroke_gradient_id})",
                stroke_widht=3,
            )
        )

        for i_column in self.groups:
            y_current = self.y_top if self.y_top is not None else 0.0
            for group in self.groups[i_column]:
                group.draw(
                    dwg=dwg, x=self.layout_configuration.paper_margin + i_column * self.layout_configuration.column_width, y=y_current
                )
                y_current += group.get_height() + self.layout_configuration.intermediate_margin

    def _get_height_for_column(self, i_column: int):
        return (
            sum([g.get_height() + self.layout_configuration.intermediate_margin for g in self.groups[i_column]])
            + self.layout_configuration.intermediate_margin
            - self.layout_configuration.small_margin
        )
