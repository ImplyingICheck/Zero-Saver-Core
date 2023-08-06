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

import decimal
from typing import Any, Literal, SupportsFloat, SupportsIndex, SupportsInt, TypeAlias, TYPE_CHECKING

import pydantic

if TYPE_CHECKING:
  from _typeshed import ReadableBuffer, SupportsTrunc

  # Most mainstream python types implement __float__. While hacky, this is a
  # good placeholder until a protocol can be defined for the methods used in
  # Item.
  NumberLike: TypeAlias = SupportsFloat
  CastableToInt = (
      str | ReadableBuffer | SupportsInt | SupportsIndex | SupportsTrunc)
else:
  from pydantic_core import core_schema

  class CastableToInt(int):

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any,
        handler: pydantic.GetCoreSchemaHandler) -> core_schema.CoreSchema:
      del source_type  # Unused
      del handler  # Unused
      return core_schema.int_schema()

  class NumberLike:

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any,
        handler: pydantic.GetCoreSchemaHandler) -> core_schema.CoreSchema:
      del source_type  # Unused
      del handler  # Unused
      return core_schema.no_info_before_validator_function(
          decimal.Decimal, core_schema.is_instance_schema(SupportsFloat))


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


def _convert_to_int(int_like: CastableToInt, error_message: str = '') -> int:
  """

  Args:
    int_like:
    error_message:

  Returns:

  Raises:
    ValueError: If *int_like* is cannot be cast into an int.
  """
  try:
    return parse_int(int_like)
  except (ValueError, OverflowError, TypeError) as e:
    raise ValueError(f'{error_message}{int_like}') from e


class Item(pydantic.BaseModel):
  """A dataclass representing the properties inherited by all items in "ZERO
  Sievert"."""
  item: str
  x: NumberLike
  y: NumberLike
  quantity: CastableToInt
  rotation: NumberLike | bool

  def model_post_init(self, __context: Any) -> None:
    self.quantity = _convert_to_int(self.quantity, 'Invalid quantity: ')
    self.rotation = parse_bool(self.rotation)


class GeneratedItem(Item):
  seen: NumberLike | bool
  durability: NumberLike
  created_from_player: NumberLike | bool

  def model_post_init(self, __context: Any) -> None:
    self.seen = parse_bool(self.seen)
    self.created_from_player = parse_bool(self.created_from_player)


class Attachments(pydantic.BaseModel):
  """BaseModel representing the "mods" section of a "ZERO Sievert" weapon,
  typically a firearm."""
  magazine: str
  stock: str
  handguard: str
  brake: str
  scope: str
  grip: str
  barrel: str
  att_1: str
  att_2: str
  att_3: str
  att_4: str


class Weapon(GeneratedItem):
  ammo_id: str
  ammo_quantity: CastableToInt
  weapon_fire_mode: Literal['automatic', 'semi_automatic', 'bolt_action']
  mods: Attachments | None

  def model_post_init(self, __context: Any) -> None:
    self.ammo_quantity = _convert_to_int(self.ammo_quantity,
                                         'Invalid ammo_quantity: ')
