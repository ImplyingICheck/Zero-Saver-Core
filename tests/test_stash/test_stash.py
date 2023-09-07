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

from zero_saver import stash

_CASES = 'case_stash.case_stash'
_STASH_PUBLIC_MODEL_PROPERTIES = ('chests',)
_STASH_PRIVATE_PROPERTIES = ()
_STASH_JSON_KEY_NAMES = ('chest',)
# Explicitly defined in the Python object
_CHEST_PUBLIC_MODEL_PROPERTIES = ('items',)
_CHEST_PRIVATE_PROPERTIES = ()
_CHEST_JSON_KEY_NAMES = ('items',)


@pytest_cases.fixture
@pytest_cases.parametrize_with_cases(
    'stash_data', cases=_CASES, prefix='stash_', has_tag=['Well-Formed']
)
def stash_fixture(stash_data):
  return stash.Stash(chest=stash_data)


@pytest_cases.fixture
@pytest_cases.parametrize_with_cases(
    'chest_data', cases=_CASES, prefix='chest_', has_tag=['Well-Formed']
)
def chest_fixture(chest_data):
  return stash.Chest(items=chest_data)


def test_stash_init_well_formed(stash_fixture):
  assert stash_fixture


def test_chest_init_well_formed(chest_fixture):
  assert chest_fixture


def parameterize_over_properties(*fixture_properties_pairs):
  for fixture, properties in fixture_properties_pairs:
    for property_ in properties:
      yield fixture, property_


class TestPydanticFunctionality:

  class TestModelDump:

    @pytest_cases.parametrize(
        'model, expected_property',
        parameterize_over_properties(
            (stash_fixture, _STASH_PUBLIC_MODEL_PROPERTIES),
            (chest_fixture, _CHEST_PUBLIC_MODEL_PROPERTIES),
        ),
    )
    def test_model_dump_contains_expected_properties(
        self, model, expected_property
    ):
      assert expected_property in model.model_dump().keys()

  class TestModelDumpJson:

    @pytest_cases.parametrize(
        'model, expected_json_key_name',
        parameterize_over_properties(
            (stash_fixture, _STASH_JSON_KEY_NAMES),
            (chest_fixture, _CHEST_JSON_KEY_NAMES),
        ),
    )
    def test_model_dump_contains_expected_properties(
        self, model, expected_json_key_name
    ):
      assert expected_json_key_name in model.model_dump(by_alias=True).keys()
