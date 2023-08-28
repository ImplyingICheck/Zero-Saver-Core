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
from typing import Literal, SupportsFloat, TypeAlias, TYPE_CHECKING

import pydantic

if TYPE_CHECKING:

  # Most mainstream python types implement __float__. While hacky, this is a
  # good placeholder until a protocol can be defined for the methods used in
  # Item.
  NumberLike: TypeAlias = SupportsFloat
else:
  NumberLike: TypeAlias = decimal.Decimal
  # This code would extend NumberLike to any number implementing __float__.
  # This is a hacky way of including most popular, commonly used number types.
  # from pydantic_core import core_schema
  # class NumberLike:
  #
  #   @classmethod
  #   def __get_pydantic_core_schema__(
  #       cls, source_type: Any,
  #       handler: pydantic.GetCoreSchemaHandler) -> core_schema.CoreSchema:
  #     del source_type  # Unused
  #     del handler  # Unused
  #     return core_schema.no_info_before_validator_function(
  #         decimal.Decimal, core_schema.is_instance_schema(SupportsFloat))


class Item(pydantic.BaseModel):
  """A dataclass representing the properties inherited by all items in "ZERO
  Sievert". Generally, zero_saver.item.GeneratedItem should be used to represent
  over zero_saver.item.Item.

  Args:
    name: A string used by "ZERO Saver" to identify an item. Functions as an
      item id. Serialized as "item", the "ZERO Sievert"-designated identity.
    x: A positional value. Represents the horizontal coordinate within the
      player inventory view.
    y: A positional value. Represents the vertical coordinate within the player
      inventory view.
    quantity: The number of an item. Items that do not stack will still possess
      a quantity value; e.g., "bread" possesses a quantity value of "1.0".
    rotation: Whether the item model should be rotated 90° anti-clockwise in the
      player inventory view.
  """
  name: str = pydantic.Field(alias='item')
  x: NumberLike
  y: NumberLike
  quantity: int
  rotation: bool


class GeneratedItem(Item):
  """Data fields common to many vanilla "ZERO Sievert" items, but not
  universally possessed.

  Almost all items will be of this class.

  Inherits from a pydantic.BaseModel.

  Args:
    seen: Represents if the item model should be obscured from the player. This
      flag is set when items are first "searched" for when looting.
    durability: Equivalent to "durability" in "ZERO Sievert". Items that do not
      display a durability value may still contain this field; e.g., "bread"
      possesses a durability value, but is always "100.0".
    created_from_player: Represents if an item was manufactured by the player
      character. Certain actions in "ZERO Sievert" use this value for
      calculations; e.g., the "Cooking" skill gives bonuses when consuming
      player-created consumables.
  """
  seen: bool
  durability: NumberLike
  created_from_player: bool


class Attachments(pydantic.BaseModel):
  """BaseModel representing the "mods" section of a "ZERO Sievert" weapon,
  typically a firearm.

  For a vanilla "ZERO Sievert" zero_saver.item.Weapon, each attribute should be
  "no_item" or a string representing the name of an attachment.
  """
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
  """BaseModel representing a weapon in "ZERO Sievert". As of "ZERO Sievert"
  version 0.31.24, only firearms contain all defined properties.

  "ZERO Saver" defines the receiver and loaded ammunition as the Weapon. All
  other components are stored in *mods*.

  Inherits from a pydantic.BaseModel.

  Args:
    ammo_id: The item name of the bullet type loaded into the weapon; e.g.,
      "ammo_545x39".
    ammo_quantity: The number of bullets currently loaded into the weapon.
    weapon_fire_mode: The firing mode currently selected.
    mods: The attachments and accessories currently equipped to the weapon.
  """
  ammo_id: str
  ammo_quantity: int
  weapon_fire_mode: Literal['automatic', 'semi_automatic', 'bolt_action']
  mods: Attachments | None


# This code would make an extensible Item, accepting any item not accounted for
# above. All methods work as expected. However, a fallback should be defined if
# the "extra" arguments have types not serialized by pydantic. Extraneous
# arguments are stored in *__pydantic_extra__*.
# class ModdedItem(Item):
#   model_config = pydantic.ConfigDict(extra='allow')

ZeroSaverItem = Weapon | GeneratedItem | Item
