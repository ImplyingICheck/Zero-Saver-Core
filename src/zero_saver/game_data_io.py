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
"""Collection of tools for accessing and working with "ZERO Sievert" save files.
Oriented towards providing tools necessary for interfacing with the OS and
presenting lexed content.

"ZERO Sievert" saves must be in the form of JSON."""
from __future__ import annotations

import contextlib
import copy
import datetime
import decimal
import enum
import hashlib
import io
import itertools
import json
import os
import pathlib
import platform
import tempfile
import winreg
import cmath
from collections.abc import Iterable, Iterator, Mapping, MutableMapping, MutableSequence, Sequence
from typing import Any, BinaryIO, Generic, Literal, overload, TextIO, TYPE_CHECKING, TypeAlias, TypeVar

from zero_saver.exceptions import winreg_errors
from zero_saver.save_golden_files import verifier
from zero_saver import monkey_patch_json

if TYPE_CHECKING:
  from _typeshed import StrOrBytesPath, StrPath
  # Missing float | int from normal JSON
  _T = TypeVar('_T')
  _S = TypeVar('_S')
  _KT = TypeVar('_KT')

  class TerminalValue(Generic[_T]):
    ...

  MutableNestedStructure: TypeAlias = (
      MutableMapping[str, 'MutableNestedStructure[_T]']
      | MutableSequence['NestedStructure[_T]']
      | TerminalValue[_T])
  NestedStructure: TypeAlias = (
      Mapping[str, 'NestedStructure[_T]'] | Sequence['NestedStructure[_T]']
      | TerminalValue[_T])
  ZeroSievertJsonValue = str | decimal.Decimal | None
  ZeroSievertSave = (
      MutableMapping[str, MutableNestedStructure[ZeroSievertJsonValue]])

# The maximum number of files located in the backup repository used by
# FileLocation. WARNING: Any files exceeding this limit will be deleted,
# starting from oldest.
MAXIMUM_NUMBER_OF_BACKUPS = 10


class WindowsArchitecture(enum.StrEnum):
  BITS_64 = '64bit'
  BITS_32 = '32bit'


def _read_registry_value(
    key_path: StrPath,
    value_name: str,
    *,
    hive: int = winreg.HKEY_LOCAL_MACHINE,
) -> str:
  if isinstance(key_path, os.PathLike):
    key_path = str(key_path)
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
    key_path = pathlib.PurePath('SOFTWARE', 'Wow6432Node', 'Valve', 'Steam')
  elif bits == WindowsArchitecture.BITS_32:
    key_path = pathlib.PurePath('SOFTWARE', 'Valve', 'Steam')
  else:
    raise ValueError(f'Unsupported architecture: {bits}')
  value_name = 'InstallPath'
  return _read_registry_value(key_path, value_name)


class FileLocation:
  """Handles retrieving path information for various files.

  This section contains OS dependent code. Though currently, only Windows10 is
  officially supported by ZERO Sievert, Zero Saver support for additional OSes
  can be added here."""
  _WINDOWS_APPDATA_PROGRAM_FILE = 'ZeroSaver'
  _WINDOWS_APPDATA_LOCAL = 'LOCALAPPDATA'
  _WINDOWS_ZERO_SIEVERT_INSTALL_PATH = pathlib.PurePath('steamapps', 'common',
                                                        'ZERO Sievert')
  _WINDOWS = 'Windows'
  _WINDOWS_BACKUPS_DIRECTORY = pathlib.PurePath(_WINDOWS_APPDATA_PROGRAM_FILE,
                                                'backup')

  def __init__(self, system: str | None = None):
    self._system: str = system if system else platform.system()
    self._generate_program_directory()
    self.save_path: pathlib.Path = self._get_save_path()
    self.backup_path: pathlib.Path = self._get_default_backup_directory()
    self.gamedata_order_path: pathlib.PurePath = self._get_gamedata_order_path()

  def _get_save_path(
      self,
      save_name: str = 'save_shared_1.dat',
  ) -> pathlib.Path:
    if self._system == 'Windows':
      root = os.getenv(self._WINDOWS_APPDATA_LOCAL, '')
      # TODO: Figure out where this number comes from. Consistent across delete
      #  and launch.
      version = '91826839'
      return pathlib.Path(root, 'ZERO_Sievert', version, save_name)
    raise ValueError(f'Unsupported operating system: {self._system}')

  def _get_gamedata_order_path(self) -> pathlib.PurePath:
    if self._system == self._WINDOWS:
      gamedata_order_file_name = 'gamedata_order.json'
      steam_install_path = _get_windows_steam_install_path()
      return pathlib.PurePath(steam_install_path,
                              self._WINDOWS_ZERO_SIEVERT_INSTALL_PATH,
                              gamedata_order_file_name)
    raise ValueError(f'Operating system not supported: {self._system}')

  def _get_default_backup_directory(self) -> pathlib.Path:
    if self._system == self._WINDOWS:
      root = os.getenv(self._WINDOWS_APPDATA_LOCAL, '')
      backup_path = pathlib.Path(root, self._WINDOWS_BACKUPS_DIRECTORY)
    else:
      raise ValueError(f'Operating system not supported: {self._system}')
    if not backup_path.exists() or not backup_path.is_dir():
      raise ValueError(f'Invalid backup location: {backup_path}')
    return backup_path

  def _generate_program_directory(self) -> None:
    if self._system == self._WINDOWS:
      root = os.getenv(self._WINDOWS_APPDATA_LOCAL, '')
      program_directory = pathlib.Path(root, self._WINDOWS_APPDATA_PROGRAM_FILE)
      try:
        program_directory.mkdir()
      except FileExistsError:
        pass
      backup_directory = pathlib.Path(root, self._WINDOWS_BACKUPS_DIRECTORY)
      try:
        backup_directory.mkdir()
      except FileExistsError:
        pass


def get_nested_value(
    dictionary: MutableNestedStructure[_T],
    keys: Iterable[str],
) -> MutableNestedStructure[_T]:
  original_dictionary = dictionary
  for key in keys:
    if not isinstance(dictionary, MutableMapping):
      raise ValueError(f'Incorrect keys passed for mapping (keys: {keys}): '
                       f'{original_dictionary}')
    dictionary = dictionary[key]
  return dictionary


def _types_match(object_1: Any, object_2: Any) -> bool:
  if not isinstance(object_1, type):
    object_1 = type(object_1)
  if not isinstance(object_2, type):
    object_2 = type(object_2)
  return object_1 == object_2


def _current_datetime_as_valid_filename() -> str:
  current_datetime = datetime.datetime.now().isoformat(
      sep='H', timespec='minutes')
  return current_datetime.replace(':', 'M')


def _iterator_length(iterator: Iterator[Any]) -> int:
  itertools_count = itertools.count()
  for iteration in zip(iterator, itertools_count):
    del iteration  # unused
  return next(itertools_count)


def _delete_oldest_file(directory: StrPath) -> None:
  """

  Args:
    directory:

  Returns:

  Raises:
    ValueError: If directory specifies a an empty directory.
  """
  oldest_time = cmath.inf
  oldest_file: os.DirEntry[str] | None = None
  for file in os.scandir(directory):
    last_modified_time = os.stat(file).st_mtime_ns
    if last_modified_time < oldest_time:
      oldest_time = last_modified_time
      oldest_file = file
  if oldest_file is None:
    raise ValueError(f'Found an empty directory: {directory}')
  try:
    os.remove(oldest_file.path)
  except FileNotFoundError:
    pass


def _files_match(*files: StrOrBytesPath, blocksize: int = 2**20) -> bool:
  """

  Args:
    *files:
    blocksize:

  Returns:

  Raises:
    IndexError: If no files are passed in.
  """
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
    base_class: type | tuple[type | tuple[Any, ...], ...] = (str, tuple),
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
  if not _types_match(object_1, object_2):
    return False
  # While object_1 and object_2 should never have differing types, these checks
  # are necessary to ensure type safety in static analysis.
  if not (isinstance(object_1, base_class) or
          isinstance(object_2, base_class)) and isinstance(
              object_1,
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
    return _types_match(object_1, object_2)
  # Recursive : Same type and all contents match
  return True


@overload
@contextlib.contextmanager
def _atomic_write(
    file_path: StrPath,
    /,
    mode: Literal['wb'] = 'wb',
    buffering: int = -1,
    encoding: str | None = None,
    errors: str | None = None,
    newline: str | None = '',
    closefd: bool = True,
    opener: Any = None,
) -> Iterator[BinaryIO]:
  ...


@overload
@contextlib.contextmanager
def _atomic_write(
    file_path: StrPath,
    /,
    mode: Literal['w'] = 'w',
    buffering: int = -1,
    encoding: str | None = None,
    errors: str | None = None,
    newline: str | None = '',
    closefd: bool = True,
    opener: Any = None,
) -> Iterator[TextIO]:
  ...


@contextlib.contextmanager
def _atomic_write(
    file_path: StrPath,
    /,
    mode: Literal['w', 'wb'] = 'w',
    buffering: int = -1,
    encoding: str | None = None,
    errors: str | None = None,
    newline: str | None = None,
    closefd: bool = True,
    opener: Any = None,
) -> Iterator[TextIO | BinaryIO]:
  directory = pathlib.PurePath(file_path).parent
  file_descriptor, temporary_file = tempfile.mkstemp(dir=directory)
  f = os.fdopen(
      file_descriptor,
      mode=mode,
      buffering=buffering,
      encoding=encoding,
      errors=errors,
      newline=newline,
      closefd=closefd,
      opener=opener)
  try:
    assert isinstance(f, (io.TextIOWrapper, io.BufferedWriter))
    yield f
  except Exception as e:
    f.close()
    os.remove(temporary_file)
    raise e
  else:
    f.flush()
    os.fsync(f.fileno())
    f.close()
  os.replace(temporary_file, file_path)


class GameDataIO:
  """Translation layer for conversion of save data and game data json into Zero
  Saver objects."""

  def __init__(
      self,
      save_path: StrPath | None = '',
      backup_path: StrPath | None = '',
  ):
    file_locations = FileLocation()
    self._save_path = pathlib.Path(
        save_path) if save_path else file_locations.save_path
    self._backup_path = (
        pathlib.Path(backup_path)
        if backup_path else file_locations.backup_path)
    self.save: ZeroSievertSave = self._read_save_file()

  def _read_save_file(self,) -> ZeroSievertSave:
    with open(self._save_path, 'r', encoding='utf-8') as f:
      return json.load(f, parse_float=decimal.Decimal)

  def _backup_save_file(self) -> bool:
    """Assumes that self._backup_path does not contain any files besides
    backups. This includes subdirectories and symbolic links.
    """
    backup_path = self._backup_path
    save_path = self._save_path
    if _iterator_length(backup_path.iterdir()) >= MAXIMUM_NUMBER_OF_BACKUPS:
      _delete_oldest_file(backup_path)
    backup_filename = (f'{save_path.name}'
                       f'{_current_datetime_as_valid_filename()}')
    backup_file_path = backup_path.joinpath(backup_filename)
    backup_path.write_bytes(save_path.read_bytes())
    return _files_match(save_path, backup_file_path)

  def write_save_file(self) -> None:
    """Overwrites the Zero Sievert save file on disk. Various possible errors
    are described in the Raises section.

    Returns:
      None.

    Raises:
      OSError: If an error occurs while handling
        zero_saver.game_data_io._atomic_write() of self._save_path.
      ValueError: If integrity checks were successfully set up, but self.save
        does not pass integrity checks. See self.verify_save_integrity() for
        implementation details.
      RuntimeError:
        If a backup of the un-edited save file is created, but their
          SHA-256 hashes do not match. See self._backup_save_file() for
          implementation details.
        If an error occurs during integrity check setup. See
          self.verify_save_integrity() for implementation details.
    """
    try:
      if not self.verify_save_integrity():
        raise ValueError(f'Save not formatted properly: {self.save}')
    except (OSError, copy.Error) as e:
      raise RuntimeError('Failed during set up of integrity check.') from e
    try:
      if not self._backup_save_file():
        raise RuntimeError('The SHA-256 hash of the written backup file and '
                           'original save file do not match.')
    except OSError as e:
      raise RuntimeError('Failed to create a backup file.') from e
    with _atomic_write(self._save_path, 'w', encoding='utf-8') as f:
      json.dump(self.save, f, cls=monkey_patch_json.ZeroSievertJsonEncoder)

  def _import_gamedata(self):
    pass

  def _remove_player_inventory(self) -> tuple[ZeroSievertSave, ZeroSievertSave]:
    """

    Returns:

    Raises:
      copy.Error: If an error occurs while copying the data field associated
        with a player inventory in a save.
    """
    inventory_representation = []
    save = self.save
    personal_inventory = ['data', 'pre_raid', 'Inventory']
    player_inventory = get_nested_value(save, personal_inventory)
    assert isinstance(player_inventory, MutableMapping)
    temp_player_inventory = copy.deepcopy(player_inventory)
    player_inventory['items'] = inventory_representation
    return player_inventory, temp_player_inventory

  def _remove_player_storage(self) -> tuple[ZeroSievertSave, ZeroSievertSave]:
    """

    Returns:

    Raises:
      copy.Error: If an error occurs while copying the data field associated
        with a player storage.
    """
    chest_representation = []
    save = self.save
    number_of_chests = 14
    player_chests = [f'chest_{index}' for index in range(number_of_chests)]
    player_storage = get_nested_value(save, ['data', 'chest'])
    assert isinstance(player_storage, MutableMapping)
    temp_player_storage = copy.deepcopy(player_storage)
    for chest in player_chests:
      player_storage[chest] = chest_representation
    return player_storage, temp_player_storage

  @contextlib.contextmanager
  def _normalize_player_inventory(self) -> Iterator[None]:
    """Removes all items in a save file. This function serves to make type
    and key comparisons between the golden file and player save file consistent
    regardless of the items acquired by the player.

    Example:
      >>> with self._normalize_player_inventory():
            do_some_stuff_with_normalized_save()
          do_some_stuff_with_original_save()

    Raises:
      copy.Error: If an error occurs while copying portions of self.save. See
        self._remove_player_inventory() and self._remove_player_storage() for
        implementation details.
    """
    player_inventory = self._remove_player_inventory()
    player_storage = self._remove_player_storage()
    try:
      yield
    finally:
      for normalized_data, original_data in [player_inventory, player_storage]:
        normalized_data.clear()
        normalized_data.update(original_data)

  def verify_save_integrity(self) -> bool:
    """Checks that a save file contains the correct, expected fields.

    Important: This function does not check if values are well-formed, only that
     they are of the expected type.

    Returns:
      A bool signifying if all keys exist, and their corresponding value types
        match.
    Raises:
      copy.Error: If an error occurs while generating a deepcopy of self.save
        values. See self._normalize_player_inventory() for implementation
        details.
      OSError: If an error occurs while handling builtins.open() of the golden
        file specified by the save version. See
        verifier.golden_save_file_from_version() for implementation details.
    """
    save_version = self.save['save_version']
    assert isinstance(save_version, str)
    with verifier.golden_save_file_from_version(save_version) as f:
      expected_save = json.load(
          f, object_hook=monkey_patch_json.parse_type_hints)
      with self._normalize_player_inventory():
        return _compare_contents(self.save, expected_save)
