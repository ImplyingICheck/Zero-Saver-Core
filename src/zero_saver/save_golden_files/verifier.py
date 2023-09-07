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
"""A collection of utility functions for accessing Zero Saver golden files.

All functions assume that verifier.py is located in the same directory as the
golden files. If that is not the case, use GOLDEN_FILE_DIRECTORY to set the root
as desired."""
from __future__ import annotations

import enum
import importlib
import pathlib
from typing import Any, TextIO, TYPE_CHECKING, TypeAlias

import pydantic
from pydantic import TypeAdapter

if TYPE_CHECKING:
  from _typeshed import StrPath

  Validator: TypeAlias = TypeAdapter[Any]

GOLDEN_FILE_DIRECTORY = str(pathlib.PurePath(__file__).parent)
ENCODING = 'utf-8'


class GoldenFilePrefix(enum.StrEnum):
  SAVE = 'key_structure_'


def open_golden_file(filename: StrPath) -> TextIO:
  """A helper function for opening golden files. Prevents the need to track
  the directory and encoding for each file.

  Args:
    filename: The complete filename, including any extension

  Examples:
    >>> with open_golden_file('the_file_you_want.json') as f:
    >>>   lines = f.readlines()

    >>> f = open_golden_file('some_file')
    >>> lines = f.readlines()
    >>> f.close()

  Returns:
    An IO object with read permissions, encoded in "utf-8".

  Raises:
    OSError: If an error occurs while handling open() of the file corresponding
      to the path: zero_saver.save_golden_files.verifier.GOLDEN_FILE_DIRECTORY
      + *filename*.
  """
  return open(
      pathlib.Path(GOLDEN_FILE_DIRECTORY, filename),
      mode='r',
      encoding=ENCODING,
  )


def golden_save_file_from_version(version: str) -> TextIO:
  """Helper function to open a golden file detailing expected save structure.

  Args:
    version: A string specifying a Zero Sievert save version. The string is
      sanitised by converting spaces to "_" and appending ".json".

  Returns:
    A TextIO stream with read permissions, encoded by
    zero_saver.save_golden_files.verifier.ENCODING.

  Raises:
    OSError: If an error occurs during open() of the file corresponding to
      *version*. See zero_saver.save_golden_files.verifier.open_golden_file()
      for implementation details.
  """
  filename = f"{GoldenFilePrefix.SAVE}{version.replace(' ', '_')}.json"
  return open_golden_file(filename)


def get_json_validator(version: str) -> Validator:
  """Interface for accessing the pydantic.TypeAdapter corresponding to a save
  *version*.

  Args:
    version: The version of the save to be validated.

  Returns:
    A pydantic.TypeAdapter corresponding to the TypedDict of *version*.
  """
  clean_version_name = version.translate(str.maketrans('. ', '__'))
  file_name = f'typed_dict_{clean_version_name}'
  module = f'zero_saver.save_golden_files.{file_name}'
  try:
    module = importlib.import_module(module)
  except ModuleNotFoundError:
    raise ModuleNotFoundError(
        f'The validation class does not exist: {module}'
    ) from None
  return pydantic.TypeAdapter(module.Model)
