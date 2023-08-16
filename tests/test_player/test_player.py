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
# pylint: disable=protected-access
import itertools
from typing import Any

import pytest_cases
import pydantic
import pytest

from zero_saver import player
from zero_saver import item

_CASES = 'case_player.case_player'
_INVENTORY_PUBLIC_MODEL_PROPERTIES = ()
_INVENTORY_PRIVATE_PROPERTIES = ()
_INVENTORY_JSON_KEY_NAMES = ()
_STATS_PUBLIC_MODEL_PROPERTIES = ('hp_max', 'stamina_max', 'x', 'y', 'wound',
                                  'hp', 'energy', 'radiation', 'fatigue',
                                  'thirst')
# Explicitly defined in the Python object
_STATS_PUBLIC_PROPERTIES = ('position',)
_STATS_PRIVATE_PROPERTIES = ()
_STATS_JSON_KEY_NAMES = ('hp_max', 'stamina_max', 'x', 'y', 'wound', 'hp',
                         'energy', 'radiation', 'fatigue', 'thirst')
_PLAYER_PUBLIC__MODEL_PROPERTIES = ('stats', 'inventory')
_PLAYER_PRIVATE_PROPERTIES = ()
_PLAYER_JSON_KEY_NAMES = ('stats', 'inventory')


class _TestComponents(pydantic.BaseModel):
  original_kwargs: dict[str, Any]


class StatsTestComponents(player.Stats, _TestComponents):
  pass


class InventoryTestComponents(player.Inventory):
  pass


class PlayerTestComponents(player.Player, _TestComponents):
  pass


@pytest_cases.fixture
@pytest_cases.parametrize_with_cases(
    'stats', cases=_CASES, has_tag=['Well-Formed'], prefix='stats_')
def stats_fixture(stats):
  return StatsTestComponents(**stats, original_kwargs=stats)


@pytest_cases.fixture
@pytest_cases.parametrize_with_cases(
    'inventory', cases=_CASES, has_tag=['Well-Formed'], prefix='inventory_')
def inventory_fixture(inventory):
  return InventoryTestComponents(inventory)


@pytest_cases.fixture
@pytest_cases.parametrize_with_cases(
    'stats', cases=_CASES, has_tag=['Well-Formed'], prefix='stats_')
@pytest_cases.parametrize_with_cases(
    'inventory', cases=_CASES, has_tag=['Well-Formed'], prefix='inventory_')
def player_fixture(stats, inventory):
  kwargs = {'stats': stats, 'inventory': inventory}
  return PlayerTestComponents(**kwargs, original_kwargs=kwargs)


class TestStats:

  def test_stats_init_well_formed(self, stats_fixture):
    assert stats_fixture

  def test_stats_position_matches_x_y_values(self, stats_fixture):
    expected_x = stats_fixture.x
    expected_y = stats_fixture.y
    assert stats_fixture.position == (expected_x, expected_y)

  def test_stats_has_position_property(self, stats_fixture):
    assert hasattr(stats_fixture, 'position')


@pytest.fixture(scope='module')
def inventory_type_adapter():
  return pydantic.TypeAdapter(player.Inventory)


class TestInventory:

  def test_inventory_init_well_formed(self, inventory_fixture):
    assert inventory_fixture

  @pytest.mark.filterwarnings('ignore::pydantic.PydanticDeprecatedSince20')
  def test_inventory_iter_traverses_items(self, mocker):
    # pydantic __fields__ is deprecated. Used by unittest.Mock() in spec call.
    expected_items = [
        mocker.Mock(spec=item.Weapon),
        mocker.Mock(spec=item.GeneratedItem),
        mocker.Mock(spec=item.Item),
    ]
    actual_inventory = player.Inventory(expected_items)
    assert actual_inventory == expected_items

  def test_inventory_empty_init_returns_empty_list(self):
    # pylint: disable=use-implicit-booleaness-not-comparison
    actual_inventory = player.Inventory()
    assert actual_inventory == []

  def test_inventory_init_validates_input(self, inventory_fixture):
    assert all(
        map(
            isinstance,
            inventory_fixture,
            itertools.repeat(item.Weapon | item.GeneratedItem | item.Item),
        ))

  def test_inventory_init_malformed_raises_validation_error(self, mocker):
    malformed_argument = mocker.Mock()
    with pytest.raises(pydantic.ValidationError):
      player.Inventory(malformed_argument)

  def test_inventory_model_dump_json_returns_string(self, inventory_fixture):
    assert isinstance(inventory_fixture.model_dump_json(), str)

  @pytest.mark.slow
  @pytest_cases.parametrize_with_cases(
      'dump_json_arguments',
      cases=_CASES,
      prefix='pydantic_dump_',
      idstyle='explicit',
      import_fixtures=True)
  def test_inventory_model_dump_json_matches_type_adapter(
      self, inventory_fixture, dump_json_arguments, inventory_type_adapter):
    expected_value = inventory_type_adapter.dump_json(inventory_fixture,
                                                      **dump_json_arguments)
    actual_value = inventory_fixture.model_dump_json(**dump_json_arguments)
    assert actual_value.encode() == expected_value


class TestPlayer:

  def test_player_init_well_formed(self, player_fixture):
    assert player_fixture

  def test_player_inventory_correct_type(self, player_fixture):
    assert isinstance(player_fixture.inventory, player.Inventory)

  def test_player_stats_correct_type(self, player_fixture):
    assert isinstance(player_fixture.stats, player.Stats)


def parameterize_over_properties(*fixture_properties_pairs):
  for fixture, properties in fixture_properties_pairs:
    for property_ in properties:
      yield fixture, property_


class TestPydanticFunctionality:

  class TestModelDump:

    @pytest_cases.parametrize(
        'model, expected_property',
        parameterize_over_properties(
            (inventory_fixture, _INVENTORY_PUBLIC_MODEL_PROPERTIES),
            (stats_fixture, _STATS_PUBLIC_MODEL_PROPERTIES),
            (player_fixture, _PLAYER_PUBLIC__MODEL_PROPERTIES)))
    def test_model_dump_contains_expected_properties(self, model,
                                                     expected_property):
      assert expected_property in model.model_dump().keys()

  class TestModelDumpJson:

    @pytest_cases.parametrize(
        'model, expected_json_key_name',
        parameterize_over_properties(
            (inventory_fixture, _INVENTORY_JSON_KEY_NAMES),
            (stats_fixture, _STATS_JSON_KEY_NAMES),
            (player_fixture, _PLAYER_JSON_KEY_NAMES)))
    def test_model_dump_contains_expected_properties(self, model,
                                                     expected_json_key_name):
      assert expected_json_key_name in model.model_dump().keys()

  class TestCustomClassTypeAdapter:

    def test_inventory_type_adapter(self,
                                    adapter=pydantic.TypeAdapter(
                                        player.Inventory)):
      assert adapter

    def test_inventory_type_adapter_has_json_schema(self,
                                                    inventory_type_adapter):
      assert inventory_type_adapter.json_schema()
