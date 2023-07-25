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
"""A collection of helper functions for working with winreg exceptions"""
import copy
import os.path
import winreg


def hkey_int_to_str(hkey: int | str) -> str:
  name_lookup: dict[int | str, str] = {
      winreg.HKEY_CLASSES_ROOT: 'HKEY_CLASSES_ROOT',
      winreg.HKEY_CURRENT_USER: 'HKEY_CURRENT_USER',
      winreg.HKEY_LOCAL_MACHINE: 'HKEY_LOCAL_MACHINE',
      winreg.HKEY_USERS: 'HKEY_USERS',
      winreg.HKEY_PERFORMANCE_DATA: 'HKEY_PERFORMANCE_DATA',
      winreg.HKEY_CURRENT_CONFIG: 'HKEY_CURRENT_CONFIG',
      winreg.HKEY_DYN_DATA: 'HKEY_DYN_DATA',
  }
  try:
    return name_lookup[hkey]
  except KeyError:
    return str(hkey)


class WinregErrorFormatter:
  """A helper class meant to format FileNotFoundError exceptions when reading
  registry values using winreg."""

  def __init__(
      self,
      winreg_error: FileNotFoundError,
      *,
      hive: int | None = None,
      key_path: str | None = None,
      value_name: str | None = '',
      shallow_copy: bool = True,
  ):
    self.winreg_error: FileNotFoundError = (
        winreg_error if shallow_copy else copy.copy(winreg_error))
    self._hive = hive if hive is not None else ''
    self._key_path = key_path if key_path is not None else ''
    self._value_name = value_name if value_name is not None else ''

  def format_as_human_readable(self) -> None:
    human_readable_hive = hkey_int_to_str(self._hive)
    full_key_path = os.path.join(human_readable_hive, self._key_path)
    if self._value_name:
      self.winreg_error.strerror = (f'The registry key does not contain the '
                                    f'value (key: {full_key_path}): '
                                    f'{self._value_name}')
    else:
      self.winreg_error.strerror = (f'The registry key does not exist: '
                                    f'{full_key_path}')
