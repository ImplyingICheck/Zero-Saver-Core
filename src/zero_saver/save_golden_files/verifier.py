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
import pathlib
from typing import TextIO, TYPE_CHECKING
if TYPE_CHECKING:
  from _typeshed import StrPath

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
    An IO object with read permissions, encoded in "utf-8"
  """
  return open(
      pathlib.Path(GOLDEN_FILE_DIRECTORY, filename),
      mode='r',
      encoding=ENCODING,
  )


def golden_save_file_from_version(version: str) -> TextIO:
  filename = f"{GoldenFilePrefix.SAVE}{version.replace(' ', '_')}.json"
  return open_golden_file(filename)
