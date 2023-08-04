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

from zero_saver import game_data_io
from zero_saver import player
from zero_saver import stash


class SaveDataFactory:
  """Abstract factory representing the methods used to parse a
  zero_saver.game_data_io.ZeroSievertSave."""

  def __init__(self, save: game_data_io.ZeroSievertSave):
    self.save = save

  def get_player(self) -> player.Player:
    raise NotImplementedError

  def get_storage(self) -> stash.Stash:
    raise NotImplementedError


class SaveData:
  """Public interface for accessing the contents of a save file."""

  def __init__(self, save: game_data_io.ZeroSievertSave):
    self.save = save
