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
"""A set of functionalities for reading in testing resources saved on disk.

Does not use any code under test."""
from __future__ import annotations

import pathlib
import simplejson
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from _typeshed import StrPath

_SAVE_FILE_DIRECTORY = pathlib.PurePath(__file__).parent.joinpath('save_files')


def serialize_save_json_from_file(file_name: StrPath):
  if pathlib.PurePath(file_name).suffix != '.json':
    file_name = f'{file_name}.json'
  file_path = _SAVE_FILE_DIRECTORY.joinpath(file_name)
  with open(file_path, encoding='utf-8') as f:
    return simplejson.load(f, use_decimal=True)
