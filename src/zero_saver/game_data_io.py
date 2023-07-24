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
"""Context manager for reading game data files from ZERO Sievert and writing
modified save files.

Working data is assumed to be in the form of JSON."""
from __future__ import annotations

import enum
import json
import os
import platform
import winreg
from typing import TYPE_CHECKING

from zero_saver.exceptions import winreg_errors

if TYPE_CHECKING:
  from _typeshed import StrOrBytesPath


class WindowsArchitecture(enum.StrEnum):
  BITS_64 = '64bit'
  BITS_32 = '32bit'


def _read_registry_value(
    key_path: str,
    value_name: str,
    *,
    hive: int = winreg.HKEY_LOCAL_MACHINE,
):
  try:
    key = winreg.OpenKey(hive, key_path)
  except FileNotFoundError as e:
    error = winreg_errors.WinregErrorFormatter(
        e,
        hive=hive,
        key_path=key_path,
    )
    error.format_as_human_readable()
    raise error.winreg_error
  try:
    value, value_type = winreg.QueryValueEx(key, value_name)
    del value_type  # unused
  except FileNotFoundError as e:
    error = winreg_errors.WinregErrorFormatter(
        e,
        hive=hive,
        key_path=key_path,
        value_name=value_name,
    )
    error.format_as_human_readable()
    raise error.winreg_error
  key.Close()
  return value


def _get_windows_steam_install_path():
  bits, linkage = platform.architecture()
  del linkage  # unused
  if bits == WindowsArchitecture.BITS_64:
    key_path = os.path.join('SOFTWARE', 'Wow6432Node', 'Valve', 'Steam')
  elif bits == WindowsArchitecture.BITS_32:
    key_path = os.path.join('SOFTWARE', 'Valve', 'Steam')
  else:
    raise ValueError(f'Unsupported architecture: {bits}')
  value_name = 'InstallPath'
  return _read_registry_value(key_path, value_name)


class FileLocation:
  """Handles retrieving path information for various files.

  This section contains OS dependent code. Though currently, only Windows10 is
  officially supported by ZERO Sievert, Zero Saver support for additional OSes
  can be added here."""
  WINDOWS_APPDATA_LOCAL = 'LOCALAPPDATA'
  WINDOWS_ZERO_SIEVERT_INSTALL_PATH = os.path.join('steamapps', 'common',
                                                   'ZERO Sievert')

  def __init__(self, system: str | None = None):
    self.system = system if system else platform.system()
    self.save_path = self._get_save_path()
    self.gamedata_order_path = self._get_gamedata_order_path()

  def _get_save_path(
      self,
      save_name: str = 'save_shared_1.dat',
  ) -> StrOrBytesPath:
    if self.system == 'Windows':
      root = os.getenv(self.WINDOWS_APPDATA_LOCAL)
      assert isinstance(root, str)
      # TODO: Figure out where this number comes from. Consistent across delete
      #  and launch.
      version = '91826839'
      save_path = os.path.join('ZERO_Sievert', version, save_name)
      return os.path.join(root, save_path)
    raise ValueError(f'Invalid operating system: {self.system}')

  def _get_gamedata_order_path(self) -> StrOrBytesPath:
    if self.system == 'Windows':
      gamedata_order_file_name = 'gamedata_order.json'
      steam_install_path = _get_windows_steam_install_path()
      return os.path.join(steam_install_path,
                          self.WINDOWS_ZERO_SIEVERT_INSTALL_PATH,
                          gamedata_order_file_name)
    raise ValueError(f'Operating system not supported: {self.system}')


def _parse_float(float_as_str: str):
  # ZERO Sievert saves encode ints as 'x.0' for some ungodly reason
  if float_as_str[-2] == '.' and float_as_str[-1] == '0':
    return int(float_as_str.split('.')[0])
  else:
    return float(float_as_str)


class GameDataIO:
  """Translation layer for conversion of save data and game data json into Zero
  Saver objects."""

  def __init__(self, save_path: StrOrBytesPath | None = ''):
    file_locations = FileLocation()
    save_path = save_path if save_path else file_locations.save_path
    self.save = self._read_save_file(save_path)

  def _read_save_file(
      self,
      save_path: StrOrBytesPath,
  ) -> dict[str, str | float]:
    with open(save_path, 'r', encoding='utf-8') as f:
      return json.load(f, parse_float=_parse_float)

  def _import_gamedata(self):
    pass
