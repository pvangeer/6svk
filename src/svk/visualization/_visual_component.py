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
from typing import Any, Self, TypeVar

from pydantic import BaseModel, PrivateAttr, model_validator

from svk.data import LinksRegister, Translator
from svk.visualization._layout_configuration import LayoutConfiguration

VisualComponentType = TypeVar("VisualComponentType", bound="VisualComponent")


class VisualComponent(BaseModel, ABC):
    _width: float = PrivateAttr(default=0.0)
    _height: float = PrivateAttr(default=0.0)

    layout_configuration: LayoutConfiguration
    """The layout configuration shared across all components of a document."""
    links_register: LinksRegister
    """The links register shared across all components of a document."""
    translator: Translator
    """The translator that should be used for this component."""

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    @model_validator(mode="after")
    def initialize_and_measure(self) -> Self:
        self.initialize()
        self.measure()
        return self

    def initialize(self) -> None:
        """Initialize component state before measuring its dimensions."""

    @abstractmethod
    def measure(self) -> None:
        """Calculate and store this component's width and height."""

    def create(self, component_type: type[VisualComponentType], **kwargs: Any) -> VisualComponentType:
        return component_type(
            **{
                **kwargs,
                "layout_configuration": self.layout_configuration,
                "links_register": self.links_register,
                "translator": self.translator,
            }
        )
