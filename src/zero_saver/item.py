#  Copyright 2023 The Zero Saver Authors. All Rights Reserved.
#
#  This file is part of Zero Saver.
#
#  Zero Saver is free software: you can redistribute it and/or modify it under
#  the terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Zero Saver is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
#  A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License along with
#  Zero Saver. If not, see <https://www.gnu.org/licenses/>.
"""Dataclasses representing various items. Define supported operations and
fields."""
from __future__ import annotations

import dataclasses
from typing import SupportsFloat, SupportsIndex, SupportsInt, TypeAlias, TYPE_CHECKING

if TYPE_CHECKING:
  from _typeshed import ReadableBuffer, SupportsTrunc

  CastableToInt = (
      str | ReadableBuffer | SupportsInt | SupportsIndex | SupportsTrunc)

# Most mainstream python types implement __float__. While hacky, this is a good
# placeholder until a protocol can be defined for the methods used in Item.
NumberLike: TypeAlias = SupportsFloat


@dataclasses.dataclass
class Item:
  """A dataclass representing the properties inherited by all items in "ZERO
  Sievert"."""
  item: str
  x: NumberLike
  y: NumberLike
  quantity: CastableToInt
  rotation: bool

  def __post_init__(self):
    self.validate_quantity()
    assert isinstance(self.quantity, int)

  def validate_quantity(self) -> None:
    quantity = self.quantity
    if not isinstance(quantity, int):
      self.quantity = int(quantity)
