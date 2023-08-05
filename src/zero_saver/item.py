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
from typing import Any, Literal, SupportsFloat, SupportsIndex, SupportsInt, TypeAlias, TYPE_CHECKING

if TYPE_CHECKING:
  from _typeshed import ReadableBuffer, SupportsTrunc

  CastableToInt = (
      str | ReadableBuffer | SupportsInt | SupportsIndex | SupportsTrunc)

# Most mainstream python types implement __float__. While hacky, this is a good
# placeholder until a protocol can be defined for the methods used in Item.
NumberLike: TypeAlias = SupportsFloat


def parse_bool(bool_like: Any) -> bool:
  if not isinstance(bool_like, bool):
    return bool(bool_like)
  else:
    return bool_like


def parse_int(int_like: CastableToInt) -> int:
  """

  Args:
    int_like:

  Returns:

  Raises:
    ValueError: If *int_like* is not a valid representation of an int.
    OverflowError: If *int_like* is too large to represent as an int.
    TypeError: If *int_like* is not of type CastableToInt.
  """
  if not isinstance(int_like, int):
    return int(int_like)
  else:
    return int_like


@dataclasses.dataclass(kw_only=True)
class Item:
  """A dataclass representing the properties inherited by all items in "ZERO
  Sievert"."""
  item: str
  x: NumberLike
  y: NumberLike
  quantity: CastableToInt
  rotation: NumberLike | bool

  def __post_init__(self):
    try:
      self.quantity = parse_int(self.quantity)
    except (ValueError, OverflowError, TypeError) as e:
      raise ValueError(f'Invalid quantity: {self.quantity}') from e
    self.rotation = parse_bool(self.rotation)


@dataclasses.dataclass(kw_only=True)
class GeneratedItem(Item):
  seen: NumberLike | bool
  durability: NumberLike
  created_from_player: NumberLike | bool

  def __post_init__(self):
    self.seen = parse_bool(self.seen)
    self.created_from_player = parse_bool(self.created_from_player)


class Attachment:
  pass


@dataclasses.dataclass(kw_only=True)
class Weapon(GeneratedItem):
  ammo_id: str
  ammo_quantity: CastableToInt
  weapon_fire_mode: Literal['automatic', 'semi_automatic', 'bolt_action']
  mods: Attachment | None
