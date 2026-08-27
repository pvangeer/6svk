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

from svgwrite import Drawing
from svk.data import PathIconElement, RectIconElement, IconElement, Icon, IconElementType
from uuid import uuid4
from pydantic import BaseModel
from abc import ABC, abstractmethod


class SvgObject(ABC, BaseModel):
    """
    This is an abstract base class for drawing svg icons.
    """

    @abstractmethod
    def create(self, dwg: Drawing):
        """
        Create the svg object

        :param dwg: The svgwrite.Drawing object that should be used to create the svg object.
        :type dwg: Drawing
        """
        pass


class Symbol(SvgObject):
    """
    This object can be used to add an svg symbol to the svgwrite.Drawing.
    """

    id: str = f"#{uuid4()}"
    """id of the symbol"""
    width: float = 300
    """Width of the symbol"""
    height: float = 300
    """Height of the symbol"""
    objects: list[SvgObject] = []
    """A list of svg objects that form the symbol"""

    def create(self, dwg: Drawing):
        """
        Retrieves the symbol from the defs of the dwg, or creates the symbol and adds it to the defs if necessary.

        :param dwg: The svgwrite.Drawing that should be used to create the symbol.
        :type dwg: Drawing
        """
        for element in dwg.defs.elements:
            if element.get_id() == self.id:
                return element

        icon_symbol = dwg.symbol(id=self.id, viewBox=f"0 0 {self.width} {self.height}")
        for svg_object in self.objects:
            icon_symbol.add(svg_object.create(dwg))
        dwg.defs.add(icon_symbol)

        return icon_symbol

    def add_to_dwg(self, dwg: Drawing, insert: tuple[float, float], size: tuple[float, float]) -> None:
        """
        Add the symbol to the defs of a dwg and use it at the specified location.

        :param dwg: The svgwrite.Drawing object
        :type dwg: Drawing
        :param insert: The location of the top left of the symbol
        :type insert: tuple[float, float]
        :param size: the target size of the symbol
        :type size: tuple[float, float]
        """
        icon_symbol = self.create(dwg)
        dwg.add(dwg.use(icon_symbol, insert=insert, size=size))


class Path(SvgObject):
    """
    An svg Path object (used to draw symbols/icons)
    """

    path_data: PathIconElement

    def create(self, dwg: Drawing):
        """
        Creates an svg Path element that can be added to a symbol or directly added to an svgwrite.Drawing.

        :param dwg: The svgwrite.Drawing object to add this Path to.
        :type dwg: Drawing
        """
        if self.path_data.transform is None:
            return dwg.path(
                d=self.path_data.d,
                fill=self.path_data.fill,
                stroke=self.path_data.stroke,
                stroke_linecap=self.path_data.stroke_linecap,
                stroke_linejoin=self.path_data.stroke_linejoin,
                stroke_width=self.path_data.stroke_width,
            )
        else:
            return dwg.path(
                d=self.path_data.d,
                fill=self.path_data.fill,
                stroke="black",
                stroke_linecap=self.path_data.stroke_linecap,
                stroke_linejoin=self.path_data.stroke_linejoin,
                stroke_width=self.path_data.stroke_width,
                transform=self.path_data.transform,
            )


class Rect(SvgObject):
    """
    An svg Rect object (used to draw symbols/icons)
    """

    rect_data: RectIconElement

    def create(self, dwg: Drawing):
        """
        Creates an svg Rect element that can be added to a symbol or directly added to an svgwrite.Drawing.

        :param dwg: The svgwrite.Drawing object to add this Path to.
        :type dwg: Drawing
        """
        return dwg.rect(
            insert=(self.rect_data.x, self.rect_data.y),
            size=(self.rect_data.width, self.rect_data.height),
            fill=self.rect_data.fill,
            stroke=self.rect_data.stroke,
            stroke_width=self.rect_data.stroke_width,
            stroke_linecap=self.rect_data.stroke_linecap,
            stroke_linejoin=self.rect_data.strok_linejoin,
        )


# TODO: This should be a separate module? This requires knowledge of the StormSurgeBarrier enum.
def draw_scaled_icon(dwg: Drawing, icon: Icon, insert: tuple[float, float], size: tuple[float, float] = (24, 24)):
    """
    This method adds and uses a symbol to represent a StormSurgeBarrier in an svgwrite.Drawing.

    :param dwg: The svgwrite.Drawing object to add the icon to.
    :type dwg: Drawing
    :param storm_surge_barrier: The storm surge barrier type to add an icon for.
    :type storm_surge_barrier: StormSurgeBarrier
    :param insert: The insert (x-position, y-position) of the left upper corner of the icon.
    :type insert: tuple[float, float]
    :param size: The size (width and height) of the desired icon
    :type size: tuple[float, float]
    """
    ico = Symbol(id=icon.id)
    ico.objects = [_create_icon_object(e) for e in icon.elements]
    ico.add_to_dwg(dwg=dwg, insert=insert, size=size)


def _create_icon_object(element: IconElement) -> SvgObject:
    if isinstance(element, PathIconElement):
        return Path(path_data=element)

    if isinstance(element, RectIconElement):
        return Rect(rect_data=element)

    raise TypeError(f"Unsupported element type: {type(element)}")
