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

import datetime
import decimal
import enum
import hashlib
import itertools
import json
import os
import platform
import winreg
import cmath
from collections.abc import Iterator, Mapping, Sequence
from typing import Any, Generic, TYPE_CHECKING, TypeAlias, TypeVar

from zero_saver.exceptions import winreg_errors
from zero_saver.save_golden_files import verifier
from zero_saver import monkey_patch_json

if TYPE_CHECKING:
  from _typeshed import StrOrBytesPath, StrPath
  # Missing float | int from normal JSON
  ZeroSievertJsonValue = (
      str | decimal.Decimal | None | list['ZeroSievertJsonValue']
      | Mapping[str, 'ZeroSievertJsonValue'])
  ZeroSievertSave = dict[str, ZeroSievertJsonValue]
  _T = TypeVar('_T')
  _S = TypeVar('_S')
  _KT = TypeVar('_KT')
  _VT_co = TypeVar('_VT_co', covariant=True)

  class TerminalValue(Generic[_T]):
    ...

  NestedStructure: TypeAlias = (
      Mapping[str, 'NestedStructure[_T]'] | Sequence['NestedStructure[_T]']
      | TerminalValue[_T])

MAXIMUM_NUMBER_OF_BACKUPS = 10


class WindowsArchitecture(enum.StrEnum):
  BITS_64 = '64bit'
  BITS_32 = '32bit'


def _read_registry_value(
    key_path: str,
    value_name: str,
    *,
    hive: int = winreg.HKEY_LOCAL_MACHINE,
) -> str:
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


def _get_windows_steam_install_path() -> StrPath:
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
  WINDOWS_APPDATA_PROGRAM_FILE = 'ZeroSaver'
  WINDOWS_APPDATA_LOCAL = 'LOCALAPPDATA'
  WINDOWS_ZERO_SIEVERT_INSTALL_PATH = os.path.join('steamapps', 'common',
                                                   'ZERO Sievert')
  WINDOWS = 'Windows'
  WINDOWS_BACKUPS_DIRECTORY = os.path.join(WINDOWS_APPDATA_PROGRAM_FILE,
                                           'backup')

  def __init__(self, system: str | None = None):
    self._system: str = system if system else platform.system()
    self._generate_program_directory()
    self.save_path: StrPath = self._get_save_path()
    self.backup_path: StrPath = self._get_default_backup_directory()
    self.gamedata_order_path: StrPath = self._get_gamedata_order_path()

  def _get_save_path(
      self,
      save_name: str = 'save_shared_1.dat',
  ) -> StrPath:
    if self._system == 'Windows':
      root = os.getenv(self.WINDOWS_APPDATA_LOCAL)
      assert isinstance(root, str)
      # TODO: Figure out where this number comes from. Consistent across delete
      #  and launch.
      version = '91826839'
      save_path = os.path.join('ZERO_Sievert', version, save_name)
      return os.path.join(root, save_path)
    raise ValueError(f'Invalid operating system: {self._system}')

  def _get_gamedata_order_path(self) -> StrPath:
    if self._system == self.WINDOWS:
      gamedata_order_file_name = 'gamedata_order.json'
      steam_install_path = _get_windows_steam_install_path()
      return os.path.join(steam_install_path,
                          self.WINDOWS_ZERO_SIEVERT_INSTALL_PATH,
                          gamedata_order_file_name)
    raise ValueError(f'Operating system not supported: {self._system}')

  def _get_default_backup_directory(self):
    if self._system == self.WINDOWS:
      root = os.getenv(self.WINDOWS_APPDATA_LOCAL)
      assert isinstance(root, str)
      backup_path = os.path.join(root, self.WINDOWS_BACKUPS_DIRECTORY)
    else:
      raise ValueError(f'Operating system not supported: {self._system}')
    if not os.path.exists(backup_path) or not os.path.isdir(backup_path):
      raise ValueError(f'Invalid backup location: {backup_path}')
    return backup_path

  def _generate_program_directory(self) -> None:
    if self._system == self.WINDOWS:
      root = os.getenv(self.WINDOWS_APPDATA_LOCAL)
      assert isinstance(root, str)
      program_directory = os.path.join(root, self.WINDOWS_APPDATA_PROGRAM_FILE)
      try:
        os.mkdir(program_directory)
      except FileExistsError:
        pass
      backup_directory = os.path.join(root, self.WINDOWS_BACKUPS_DIRECTORY)
      try:
        os.mkdir(backup_directory)
      except FileExistsError:
        pass


def _parse_float_as_decimal(float_as_str: str) -> decimal.Decimal:
  # ZERO Sievert saves encoded ints as 'x.0' for some ungodly reason
  return decimal.Decimal(float_as_str)


def _current_datetime_as_valid_filename() -> str:
  current_datetime = datetime.datetime.now().isoformat(
      sep='H', timespec='minutes')
  return current_datetime.replace(':', 'M')


def _iterator_length(iterator: Iterator[Any]) -> int:
  itertools_count = itertools.count()
  for iteration in zip(iterator, itertools_count):
    del iteration  # unused
  return next(itertools_count)


def delete_oldest_file(directory: StrPath) -> bool:
  oldest_time = cmath.inf
  oldest_file = None
  for file in os.scandir(directory):
    last_modified_time = os.stat(file).st_mtime_ns
    if last_modified_time < oldest_time:
      oldest_time = last_modified_time
      oldest_file = file
  if oldest_file is not None:
    try:
      os.remove(oldest_file.path)
    except FileNotFoundError:
      pass
  return True


def files_match(*files: StrOrBytesPath, blocksize: int = 2**20) -> bool:
  hashes: list[bytes] = []
  for file in files:
    hash_function = hashlib.sha256()
    with open(file, 'rb') as f:
      while chunk := f.read(blocksize):
        hash_function.update(chunk)
    hashes.append(hash_function.digest())
  return hashes.count(hashes[0]) == len(hashes)


def _compare_contents(
    object_1: NestedStructure[_T],
    object_2: NestedStructure[_S],
) -> bool:
  """Strict comparison between two nested objects. Every nested item must be of
  the same type, not just share a common super class.

  Assumes that any list objects have the same order of contained items.

  Args:
    object_1:
    object_2:

  Returns:

  """
  # pylint: disable=[unidiomatic-typecheck]
  # Base case: Types do not match
  if type(object_1) != type(object_2):
    return False
  # While object_1 and object_2 should never have differing types, these checks
  # are necessary to ensure type safety in static analysis.
  if isinstance(object_1,
                (Mapping, Sequence)) and isinstance(object_2,
                                                    (Mapping, Sequence)):
    if len(object_1) != len(object_2):
      # Base case: Unequal number of keys
      return False
    if isinstance(object_1, Mapping) and isinstance(object_2, Mapping):
      try:
        values = [(object_1[key], object_2[key]) for key in object_1]
      except KeyError:
        # Base case: key in object_1 is not in object_2
        return False
    elif isinstance(object_1, Sequence) and isinstance(object_2, Sequence):
      values = zip(object_1, object_2)
    else:
      raise ValueError(f'Invalid type combination.\n'
                       f'(object_1 of type: {type(object_1)})\n'
                       f'(object_2 of type: {type(object_2)})')
    for value_1, value_2 in values:
      # Short circuit: Return false if any seen value has been False
      if not _compare_contents(value_1, value_2):
        return False
  else:
    # Base Case: Type of TerminalValue in NestedStructure matches
    return type(object_1) == type(object_2)
  # Recursive : Same type and all contents match
  return True


class GameDataIO:
  """Translation layer for conversion of save data and game data json into Zero
  Saver objects."""

  def __init__(
      self,
      save_path: StrPath | None = '',
      backup_path: StrPath | None = '',
  ):
    file_locations = FileLocation()
    self._save_path = save_path if save_path else file_locations.save_path
    self._backup_path = (
        backup_path if backup_path else file_locations.backup_path)
    self.save: ZeroSievertSave = self._read_save_file()

  def _read_save_file(self,) -> ZeroSievertSave:
    with open(self._save_path, 'r', encoding='utf-8') as f:
      return json.load(f, parse_float=_parse_float_as_decimal)

  def _backup_save_file(self) -> bool:
    backup_path = self._backup_path
    blocksize = 2**20
    if _iterator_length(os.scandir(backup_path)) >= MAXIMUM_NUMBER_OF_BACKUPS:
      assert delete_oldest_file(backup_path)
    with open(self._save_path, 'rb') as save_file:
      original_save_filename = os.path.basename(self._save_path)
      backup_filename = (f'{original_save_filename}'
                         f'{_current_datetime_as_valid_filename()}')
      backup_file_path = os.path.join(backup_path, backup_filename)
      with open(backup_file_path, mode='wb') as backup:
        while chunk := save_file.read(blocksize):
          backup.write(chunk)
    return files_match(self._save_path, backup_file_path)

  def write_save_file(self) -> None:
    assert self._backup_save_file()
    with open(self._save_path, 'w', encoding='utf-8') as f:
      json.dump(self.save, f, cls=monkey_patch_json.ZeroSievertJsonEncoder)

  def _import_gamedata(self):
    pass
