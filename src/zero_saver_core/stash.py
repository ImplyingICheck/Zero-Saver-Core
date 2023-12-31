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
"""Stub file of a class representing chest items (alias: Storage, Stash) from a
"Zero Sievert" save."""
from typing import TypeAlias

import pydantic

from zero_saver_core import item

ZeroSaverItem: TypeAlias = item.ZeroSaverItem
NumberLike: TypeAlias = item.NumberLike


class Chest(pydantic.BaseModel):
  items: list[ZeroSaverItem]


class StorageData(pydantic.BaseModel):
  slot_now: NumberLike = pydantic.Field(alias='slot now')


class Stash(pydantic.BaseModel):
  chests: dict[str, Chest | StorageData] = pydantic.Field(alias='chest')
