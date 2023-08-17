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
"""Parsing layer"""
from __future__ import annotations

import typing

from zero_saver import game_data_io
from zero_saver import player
from zero_saver import stash
from zero_saver import quest
from zero_saver import difficulty_settings
from zero_saver.save_golden_files import typed_dict_0_31_production


def get_save_version(save: game_data_io.ZeroSievertSave) -> str:
  save_version = save['save_version']
  assert isinstance(save_version, str)
  return save_version


class SaveDataFactory:
  """Abstract factory representing the methods used to parse a
  zero_saver.game_data_io.ZeroSievertSave."""

  def __init__(self, save: game_data_io.ZeroSievertSave):
    self.save = save

  def get_player(self) -> player.Player:
    raise NotImplementedError

  def get_storage(self) -> stash.Stash:
    raise NotImplementedError

  def get_quest_flags(self) -> quest.Quest:
    raise NotImplementedError

  def get_difficulty_settings(self) -> difficulty_settings.DifficultySettings:
    raise NotImplementedError

  def set_player(self, player_data: player.Player) -> None:
    raise NotImplementedError

  def set_storage(self, storage_data: stash.Stash) -> None:
    raise NotImplementedError

  def set_quest_flags(self, quest_data: quest.Quest) -> None:
    raise NotImplementedError

  def set_difficulty_settings(
      self,
      difficulty_settings_data: difficulty_settings.DifficultySettings,
  ) -> None:
    raise NotImplementedError


# Begin concrete SaveDataFactory classes


class Version031Production(SaveDataFactory):
  """A concrete SaveDataFactory for reading saves of version 0.31 production."""
  SUPPORTED_VERSIONS = frozenset(['0.31 production'])

  def get_player(self) -> player.Player:
    player_stats = self.save['data']['pre_raid']['player']
    player_inventory = self.save['data']['pre_raid']['Inventory']['items']
    return player.Player(
        stats=typing.cast(player.Stats, player_stats),
        inventory=typing.cast(player.Inventory, player_inventory))

  def set_player(self, player_data: player.Player) -> None:
    player_stats = self.save['data']['pre_raid']['player']
    player_inventory = self.save['data']['pre_raid']['Inventory']
    player_stats.update(
        typing.cast(typed_dict_0_31_production.Player,
                    player_data.stats.model_dump()))
    player_inventory['items'] = player_data.inventory.model_dump(by_alias=True)


# End concrete SaveDataFactory classes


class SaveData:
  """Public interface for accessing the contents of a save file."""

  def __init__(self, save: game_data_io.ZeroSievertSave):
    try:
      save_version = get_save_version(save)
    except (TypeError, KeyError) as e:
      raise ValueError(f'Invalid save: {save}') from e
    if save_version in Version031Production.SUPPORTED_VERSIONS:
      factory = Version031Production(save)
    else:
      raise ValueError(f'Unsupported save version: {save_version}')
    self._factory = factory
    self.player = factory.get_player()
