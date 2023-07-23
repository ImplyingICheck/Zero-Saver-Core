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

import platform
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from _typeshed import StrOrBytesPath


class FileLocation:
  """Handles retrieving path information for various files.

  This section contains OS dependent code. Though currently, only Windows10 is
  officially supported by ZERO Sievert, Zero Saver support for additional OSes
  can be added here."""

  def __init__(self, system: str):
    self.system = system if system else platform.system()
    self.save_path = self.get_save_path()
    self.gamedata_order_path = self.get_gamedata_order_path()

  def get_save_path(self) -> StrOrBytesPath:
    return ''

  def get_gamedata_order_path(self) -> StrOrBytesPath:
    return ''


class GameDataIO:
  pass
