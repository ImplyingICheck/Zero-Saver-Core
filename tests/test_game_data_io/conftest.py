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
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
import io

import pytest


class FileLikeStringIO(io.StringIO):

  def __call__(self, *args, **kwargs):
    """Mimics call to open()"""
    del args  # unused
    del kwargs  # unused
    return self

  def close(self) -> None:
    """Prevent closure by context managers."""
    pass

  def go_to_start(self):
    self.seek(0, 0)

  def true_close(self):
    super().close()


@pytest.fixture
def file_like_fixture():
  in_memory_file = FileLikeStringIO()
  yield in_memory_file
  in_memory_file.true_close()
