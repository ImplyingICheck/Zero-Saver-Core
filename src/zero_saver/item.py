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
from typing import Any, Literal, SupportsFloat, TypeAlias, TYPE_CHECKING

import pydantic

if TYPE_CHECKING:

  # Most mainstream python types implement __float__. While hacky, this is a
  # good placeholder until a protocol can be defined for the methods used in
  # Item.
  NumberLike: TypeAlias = SupportsFloat
else:
  from pydantic_core import core_schema

  class NumberLike:

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any,
        handler: pydantic.GetCoreSchemaHandler) -> core_schema.CoreSchema:
      del source_type  # Unused
      del handler  # Unused
      return core_schema.no_info_before_validator_function(
          decimal.Decimal, core_schema.is_instance_schema(SupportsFloat))


class Item(pydantic.BaseModel):
  """A dataclass representing the properties inherited by all items in "ZERO
  Sievert"."""
  item: str
  x: NumberLike
  y: NumberLike
  quantity: int
  rotation: bool


class GeneratedItem(Item):
  seen: bool
  durability: NumberLike
  created_from_player: bool


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
  ammo_quantity: int
  weapon_fire_mode: Literal['automatic', 'semi_automatic', 'bolt_action']
  mods: Attachments | None
