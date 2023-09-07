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
import pytest_cases

from resources import file_util


class SaveFileCase:

  @pytest_cases.case(tags=['SaveFilePath', 'Well-Formed'])
  @pytest_cases.parametrize(
      'file_name',
      (
          '0_31_save_new_custom_maxsettings_equipment1',
          '0_31_save_new_custom_minsettings_equipment1',
          '0_31_save_new_hunter_equipment1',
          '0_31_save_new_rookie_equipment1',
          '0_31_save_new_survivor_equipment1',
      ),
  )
  def save_file_path_well_formed(self, file_name):
    return file_util.full_file_path(file_name)
