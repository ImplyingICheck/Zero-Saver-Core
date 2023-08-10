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
from typing import TypeAlias

import pydantic

from zero_saver import item

NumberLike: TypeAlias = item.NumberLike


class Inventory(pydantic.BaseModel):
  items: list[item.Weapon | item.GeneratedItem | item.Item]


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
  def position(self):
    return self.x, self.y


class Player(pydantic.BaseModel):
  """The intended public interface for modifying values related to the player
  character."""
  stats: Stats
  inventory: Inventory
