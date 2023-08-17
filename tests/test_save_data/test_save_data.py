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
import copy

import pytest
import pytest_cases.filters

from zero_saver import save_data
from zero_saver import player

_CASES = 'case_save_data.case_save_data'


@pytest_cases.fixture
@pytest_cases.parametrize_with_cases(
    'save', cases=_CASES, has_tag=['Well-Formed'], prefix='save_json')
def save_data_fixture(save):
  return save_data.SaveData(save)


class TestSaveData:

  @pytest_cases.parametrize_with_cases(
      'save', cases=_CASES, has_tag=['Well-Formed'], prefix='save_json')
  def test_save_data_init_well_formed(self, save):
    assert save_data.SaveData(save)

  @pytest_cases.parametrize_with_cases(
      'save', cases=_CASES, has_tag=['Malformed'], prefix='save_json')
  def test_save_data_init_malformed_save_raises_value_error(self, save):
    with pytest.raises(ValueError):
      assert save_data.SaveData(save)

  @pytest_cases.parametrize_with_cases(
      'save', cases=_CASES, has_tag=['Malformed'], prefix='save_json')
  def test_save_data_init_malformed_save_correct_error_message(self, save):
    with pytest.raises(ValueError, match='Invalid save'):
      assert save_data.SaveData(save)

  def test_save_data_init_unsupported_version_raises_value_error(self, mocker):
    save = mocker.MagicMock()
    save.__getitem__.return_value = 'THIS IS NOT A SUPPORTED SAVE VERSION :('
    with pytest.raises(ValueError):
      assert save_data.SaveData(save)

  def test_save_data_init_unsupported_version_correct_error_message(
      self, mocker):
    save = mocker.MagicMock()
    save.__getitem__.return_value = 'THIS IS NOT A SUPPORTED SAVE VERSION :('
    with pytest.raises(ValueError, match='Unsupported save version'):
      assert save_data.SaveData(save)

  @pytest_cases.parametrize('expected_properties', ['_factory', 'player'])
  def test_save_data_has_expected_properties(self, save_data_fixture,
                                             expected_properties):
    assert hasattr(save_data_fixture, expected_properties)


@pytest_cases.fixture(scope='module')
@pytest_cases.parametrize_with_cases(
    'save',
    cases=_CASES,
    has_tag=['Well-Formed'],
    scope='module',
    prefix='save_json')
def save_file_fixture(save):
  return save


@pytest_cases.fixture
def save_data_factory_fixture(save_file_fixture):
  return save_data.SaveDataFactory(save_file_fixture)


class TestSaveDataFactory:

  @pytest_cases.parametrize_with_cases('save', cases=_CASES, prefix='save_json')
  def test_save_data_factory_init(self, save):
    assert save_data.SaveDataFactory(save)

  def test_save_data_factory_get_player(self, save_data_factory_fixture):
    with pytest.raises(NotImplementedError):
      save_data_factory_fixture.get_player()

  def test_save_data_factory_get_storage(self, save_data_factory_fixture):
    with pytest.raises(NotImplementedError):
      save_data_factory_fixture.get_storage()

  def test_save_data_factory_get_quest_flags(self, save_data_factory_fixture):
    with pytest.raises(NotImplementedError):
      save_data_factory_fixture.get_quest_flags()

  def test_save_data_factory_get_difficulty_settings(self,
                                                     save_data_factory_fixture):
    with pytest.raises(NotImplementedError):
      save_data_factory_fixture.get_difficulty_settings()

  def test_save_data_factory_set_player_mock(self, save_data_factory_fixture,
                                             mocker):
    player = mocker.Mock()
    with pytest.raises(NotImplementedError):
      save_data_factory_fixture.set_player(player)

  def test_save_data_factory_set_storage_mock(self, save_data_factory_fixture,
                                              mocker):
    storage = mocker.Mock()
    with pytest.raises(NotImplementedError):
      save_data_factory_fixture.set_storage(storage)

  def test_save_data_factory_set_quest_flags_mock(self,
                                                  save_data_factory_fixture,
                                                  mocker):
    storage = mocker.Mock()
    with pytest.raises(NotImplementedError):
      save_data_factory_fixture.set_quest_flags(storage)

  def test_save_data_factory_set_difficulty_settings_mock(
      self, save_data_factory_fixture, mocker):
    storage = mocker.Mock()
    with pytest.raises(NotImplementedError):
      save_data_factory_fixture.set_difficulty_settings(storage)


@pytest_cases.fixture
def version_031_production_fixture(save_file_fixture):
  return save_data.Version031Production(save_file_fixture)


class TestVersion031Production:

  def test_version_031_production_has_supported_versions_version_031_production(
      self):
    assert ('0.31 production'
            in save_data.Version031Production.SUPPORTED_VERSIONS)

  def test_version_031_production_supported_versions_is_frozenset(self):
    assert isinstance(save_data.Version031Production.SUPPORTED_VERSIONS,
                      frozenset)

  def test_version_031_production_get_player_returns_correct_type(
      self, version_031_production_fixture):
    player_data = version_031_production_fixture.get_player()
    assert isinstance(player_data, player.Player)

  def test_version_031_production_set_player_stable_round_trip(
      self, version_031_production_fixture):
    original_save = copy.deepcopy(version_031_production_fixture.save)
    player_data = version_031_production_fixture.get_player()
    version_031_production_fixture.set_player(player_data)
    assert version_031_production_fixture.save == original_save

  @pytest_cases.parametrize_with_cases(
      'stats', cases='case_player.case_player', prefix='stats_')
  def test_version_031_production_set_player_updates_stats(
      self, mocker, version_031_production_fixture, stats):
    player_data = version_031_production_fixture.get_player()
    mocked_stats = mocker.Mock(spec=player.Stats)
    mocked_stats.model_dump = lambda: stats
    player_data.stats = mocked_stats
    version_031_production_fixture.set_player(player_data)
    actual_data = version_031_production_fixture.save['data']['pre_raid'][
        'player']
    assert actual_data == stats

  @pytest_cases.parametrize_with_cases(
      'inventory', cases='case_player.case_player', prefix='inventory_')
  def test_version_031_production_set_player_updates_inventory(
      self, mocker, version_031_production_fixture, inventory):
    player_data = version_031_production_fixture.get_player()
    mocked_inventory = mocker.Mock(spec=dir(player.Inventory))
    mocked_inventory.model_dump = lambda by_alias: inventory
    player_data.inventory = mocked_inventory
    version_031_production_fixture.set_player(player_data)
    actual_data = version_031_production_fixture.save['data']['pre_raid'][
        'Inventory']['items']
    assert actual_data == inventory


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
