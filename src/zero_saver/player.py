# Copyright 2023 The Zero Saver Authors. All Rights Reserved.
#
# This file is part of Zero Saver.
#
# Zero Saver is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Zero Saver is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Zero Saver. If not, see <https://www.gnu.org/licenses/>.
"""Data structure representing player character data.

The values supported are money quantity, faction reputation,
fatigue/health/stamina/radiation values, skills, inventory, equipment, and
character metadata.
"""
from __future__ import annotations

from collections.abc import Iterable
from typing import Any, TypeAlias

import pydantic
from pydantic_core import core_schema

from zero_saver import item

NumberLike: TypeAlias = item.NumberLike


class Inventory(list[item.Weapon | item.GeneratedItem | item.Item]):
  """An interface for interacting with the inventory of a player character.
  Contains methods useful for transforming contained items.

  Additionally, provides methods defined by python list.
  """

  @classmethod
  def __get_pydantic_core_schema__(
      cls, source_type: Any,
      handler: pydantic.GetCoreSchemaHandler) -> core_schema.CoreSchema:
    del source_type  # unused
    validation_schema = handler(list[item.Weapon | item.GeneratedItem
                                     | item.Item])
    return core_schema.no_info_after_validator_function(
        cls, schema=validation_schema)

  @pydantic.validate_call
  def __init__(self,
               iterable: Iterable[item.Weapon | item.GeneratedItem
                                  | item.Item] = (),
               /):
    super().__init__(iterable)

  def model_dump_json(self,
                      *,
                      indent: int | None = None,
                      include: pydantic.main.IncEx = None,
                      exclude: pydantic.main.IncEx = None,
                      by_alias: bool = False,
                      exclude_unset: bool = False,
                      exclude_defaults: bool = False,
                      exclude_none: bool = False,
                      round_trip: bool = False,
                      warnings: bool = True) -> str:
    return pydantic.TypeAdapter(Inventory).dump_json(
        self,
        indent=indent,
        include=include,
        exclude=exclude,
        by_alias=by_alias,
        exclude_unset=exclude_unset,
        exclude_defaults=exclude_defaults,
        exclude_none=exclude_none,
        round_trip=round_trip,
        warnings=warnings).decode(encoding='utf-8')

  @pydantic.validate_call()
  def append(self, object_: item.Weapon | item.GeneratedItem | item.Item,
             /) -> None:
    super().append(object_)


class Skill:
  pass


class Equipment:
  pass


class Metadata:
  pass


class Reputation:
  pass


class Stats(pydantic.BaseModel):
  """Represents data pertaining to the player character."""
  hp_max: NumberLike
  stamina_max: NumberLike
  x: NumberLike
  y: NumberLike
  wound: NumberLike
  hp: NumberLike
  energy: NumberLike
  radiation: NumberLike
  fatigue: NumberLike
  thirst: NumberLike

  @property
  def position(self) -> tuple[NumberLike, NumberLike]:
    return self.x, self.y


class Player(pydantic.BaseModel):
  """The intended public interface for modifying values related to the player
  character."""
  stats: Stats
  inventory: Inventory
