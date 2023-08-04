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
import pytest
import pytest_cases

from zero_saver import save_data

_CASES = 'test_save_data.case_save_data'


@pytest_cases.parametrize_with_cases('save', cases=_CASES, prefix='save_json')
def test_save_data_init(save):
  assert save_data.SaveData(save)


@pytest_cases.parametrize_with_cases('save', cases=_CASES, prefix='save_json')
def test_save_data_factory_init(save):
  assert save_data.SaveDataFactory(save)


@pytest_cases.fixture
@pytest_cases.parametrize_with_cases('save', cases=_CASES, prefix='save_json')
def save_data_factory(save):
  return save_data.SaveDataFactory(save)


def test_save_data_factory_get_player(save_data_factory):
  with pytest.raises(NotImplementedError):
    save_data_factory.get_player()


def test_save_data_factory_get_storage(save_data_factory):
  with pytest.raises(NotImplementedError):
    save_data_factory.get_storage()


def test_save_data_factory_get_quest_flags(save_data_factory):
  with pytest.raises(NotImplementedError):
    save_data_factory.get_quest_flags()
