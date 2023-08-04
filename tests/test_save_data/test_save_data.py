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
import pytest_cases.filters

from zero_saver import save_data

_CASES = 'test_save_data.case_save_data'


@pytest_cases.fixture
@pytest_cases.parametrize_with_cases(
    'save', cases=_CASES, has_tag=['Well-Formed'], prefix='save_json')
def save_data_fixture(save):
  return save_data.SaveData(save)


@pytest_cases.parametrize_with_cases(
    'save', cases=_CASES, has_tag=['Well-Formed'], prefix='save_json')
def test_save_data_init_well_formed(save):
  assert save_data.SaveData(save)


@pytest_cases.parametrize('expected_properties', ['_factory'])
def test_save_data_has_expected_properties(save_data_fixture,
                                           expected_properties):
  assert hasattr(save_data_fixture, expected_properties)


@pytest_cases.fixture
@pytest_cases.parametrize_with_cases('save', cases=_CASES, prefix='save_json')
def save_data_factory(save):
  return save_data.SaveDataFactory(save)


class TestSaveDataFactory:

  @pytest_cases.parametrize_with_cases('save', cases=_CASES, prefix='save_json')
  def test_save_data_factory_init(self, save):
    assert save_data.SaveDataFactory(save)

  def test_save_data_factory_get_player(self, save_data_factory):
    with pytest.raises(NotImplementedError):
      save_data_factory.get_player()

  def test_save_data_factory_get_storage(self, save_data_factory):
    with pytest.raises(NotImplementedError):
      save_data_factory.get_storage()

  def test_save_data_factory_get_quest_flags(self, save_data_factory):
    with pytest.raises(NotImplementedError):
      save_data_factory.get_quest_flags()

  def test_save_data_factory_get_difficulty_settings(self, save_data_factory):
    with pytest.raises(NotImplementedError):
      save_data_factory.get_difficulty_settings()

  def test_save_data_factory_set_player_mock(self, save_data_factory, mocker):
    player = mocker.Mock()
    with pytest.raises(NotImplementedError):
      save_data_factory.set_player(player)

  def test_save_data_factory_set_storage_mock(self, save_data_factory, mocker):
    storage = mocker.Mock()
    with pytest.raises(NotImplementedError):
      save_data_factory.set_storage(storage)

  def test_save_data_factory_set_quest_flags_mock(self, save_data_factory,
                                                  mocker):
    storage = mocker.Mock()
    with pytest.raises(NotImplementedError):
      save_data_factory.set_quest_flags(storage)

  def test_save_data_factory_set_difficulty_settings_mock(
      self, save_data_factory, mocker):
    storage = mocker.Mock()
    with pytest.raises(NotImplementedError):
      save_data_factory.set_difficulty_settings(storage)


def test_version_031_production_has_supported_versions_version_031_production():
  assert '0.31 production' in save_data.Version031Production.SUPPORTED_VERSIONS


def test_version_031_production_supported_versions_is_frozenset():
  assert isinstance(save_data.Version031Production.SUPPORTED_VERSIONS,
                    frozenset)


def expected_save_version(save):
  return save['save_version']


class TestGetSaveVersion:

  @pytest_cases.parametrize_with_cases(
      'save', cases=_CASES, has_tag=['Well-Formed'], prefix='save_json')
  def test_get_save_version_well_formed_returns_correct_version(self, save):
    assert save_data.get_save_version(save) == expected_save_version(save)

  @pytest_cases.parametrize_with_cases(
      'save', cases=_CASES, has_tag=['Well-Formed'], prefix='save_json')
  def test_get_save_version_well_formed_returns_string(self, save):
    assert isinstance(save_data.get_save_version(save), str)

  @pytest_cases.parametrize_with_cases(
      'save',
      cases=_CASES,
      has_tag=['Malformed', 'Subscriptable'],
      prefix='save_json')
  def test_get_save_version_malformed_subscriptable_raises_key_error(
      self, save):
    with pytest.raises(KeyError):
      save_data.get_save_version(save)

  @pytest_cases.parametrize_with_cases(
      'save',
      cases=_CASES,
      filter=pytest_cases.filters.has_tag('Malformed')
      & ~pytest_cases.filters.has_tag('Subscriptable'),
      prefix='save_json')
  def test_get_save_version_malformed_not_subscriptable_raises_type_error(
      self, save):
    with pytest.raises(TypeError):
      save_data.get_save_version(save)
