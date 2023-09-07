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
# pylint: disable=redefined-outer-name
import pytest_cases

from resources import file_util


class SaveDataTestingComponents:
  save = None

  def __init__(self, save):
    self.save = save


class SaveFileJsonCase:

  @pytest_cases.case(
      tags=[
          'Well-Formed',
          'SaveJson',
          'Custom',
          'Equipment::1',
          'Maximum',
          'Version::0.31',
      ]
  )
  def save_json_0_31_save_new_custom_maxsettings_equipment1(self):
    return file_util.serialize_save_json_from_file(
        '0_31_save_new_custom_maxsettings_equipment1'
    )

  @pytest_cases.case(
      tags=[
          'Well-Formed',
          'SaveJson',
          'Custom',
          'Equipment::1',
          'Minimum',
          'Version::0.31',
      ]
  )
  def save_json_0_31_save_new_custom_minsettings_equipment1(self):
    return file_util.serialize_save_json_from_file(
        '0_31_save_new_custom_minsettings_equipment1'
    )

  @pytest_cases.case(
      tags=[
          'Well-Formed',
          'SaveJson',
          'Default',
          'Hunter',
          'Equipment::1',
          'Version::0.31',
      ]
  )
  def save_json_0_31_save_new_hunter_equipment1(self):
    return file_util.serialize_save_json_from_file(
        '0_31_save_new_hunter_equipment1'
    )

  @pytest_cases.case(
      tags=[
          'Well-Formed',
          'SaveJson',
          'Default',
          'Rookie',
          'Equipment::1',
          'Version::0.31',
      ]
  )
  def save_json_0_31_save_new_rookie_equipment1(self):
    return file_util.serialize_save_json_from_file(
        '0_31_save_new_rookie_equipment1'
    )

  @pytest_cases.case(
      tags=[
          'Well-Formed',
          'SaveJson',
          'Default',
          'Survivor',
          'Equipment::1',
          'Version::0.31',
      ]
  )
  def save_json_0_31_save_new_survivor_equipment1(self):
    return file_util.serialize_save_json_from_file(
        '0_31_save_new_survivor_equipment1'
    )

  @pytest_cases.case(
      tags=['Malformed', 'SaveJson', 'Subscriptable'], id='empty_dict'
  )
  def save_json_empty_dict(self):
    return {}

  @pytest_cases.case(tags=['Malformed', 'SaveJson', 'Subscriptable'])
  def save_json_foo_key_bar_value(self):
    return {'foo': 'bar'}

  @pytest_cases.case(tags=['Malformed', 'SaveJson', 'None'])
  def save_json_none(self):
    return None

  @pytest_cases.case(tags=['Malformed', 'SaveJson', 'WrongType'])
  def save_json_wrong_type_list(self):
    return []
