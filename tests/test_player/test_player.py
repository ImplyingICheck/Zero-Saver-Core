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
from typing import Any

import pydantic
import pytest_cases

from zero_saver import player

_CASES = 'case_player.case_player'
_INVENTORY_PUBLIC_MODEL_PROPERTIES = ('items',)
_INVENTORY_PRIVATE_PROPERTIES = ()
_INVENTORY_JSON_KEY_NAMES = ('items',)
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


class InventoryTestComponents(player.Inventory, _TestComponents):
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
  return InventoryTestComponents(**inventory, original_kwargs=inventory)


@pytest_cases.fixture
@pytest_cases.parametrize_with_cases(
    'stats', cases=_CASES, has_tag=['Well-Formed'], prefix='stats_')
@pytest_cases.parametrize_with_cases(
    'inventory', cases=_CASES, has_tag=['Well-Formed'], prefix='inventory_')
def player_fixture(stats, inventory):
  kwargs = {'stats': stats, 'inventory': inventory}
  return PlayerTestComponents(**kwargs, original_kwargs=kwargs)


def test_stats_init_well_formed(stats_fixture):
  assert stats_fixture


def test_stats_position_matches_x_y_values(stats_fixture):
  expected_x = stats_fixture.x
  expected_y = stats_fixture.y
  assert stats_fixture.position == (expected_x, expected_y)


def test_stats_has_position_property(stats_fixture):
  assert hasattr(stats_fixture, 'position')


def test_inventory_init_well_formed(inventory_fixture):
  assert inventory_fixture


def test_player_init_well_formed(player_fixture):
  assert player_fixture


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
    pass
