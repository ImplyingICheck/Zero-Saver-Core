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

import pathlib
from typing import TextIO, TYPE_CHECKING
if TYPE_CHECKING:
  from _typeshed import StrPath

GOLDEN_FILE_DIRECTORY = str(pathlib.PurePath(__file__).parent)
ENCODING = 'utf-8'


def read_golden_file(filename: StrPath) -> TextIO:
  with open(
      pathlib.Path(
          GOLDEN_FILE_DIRECTORY,
          filename,
      ),
      mode='r',
      encoding=ENCODING) as f:
    return f
