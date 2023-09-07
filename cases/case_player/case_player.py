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
import pydantic
import pytest_cases.filters

from zero_saver import item


class StatsCase:

  @pytest_cases.case(tags=['Stats', 'Well-Formed'])
  def stats_fresh_spawn_well_formed(self):
    return {
        'hp_max': 120.0,
        'stamina_max': 100.0,
        'x': 323.99322509765625,
        'wound': 0.0,
        'y': 873.85711669921875,
        'hp': 120.0,
        'energy': 90.0,
        'radiation': 0.0,
        'fatigue': 97.632510444442118568986188620329,
        'thirst': 90.0,
    }


class InventoryCase:

  @pytest_cases.case(tags=['Inventory', 'Well-Formed', 'ExternalCases'])
  @pytest_cases.parametrize_with_cases(
      'item_',
      cases='case_item.case_item',
      has_tag=['Well-Formed'],
      prefix=('weapon_', 'generated_item_', 'item_'),  # type: ignore
  )  # type: ignore
  def inventory_single_well_formed_item(self, item_):
    return [item_]

  @pytest_cases.case(
      tags=['TupleTestValue', 'Item', 'Well-Formed', 'ExternalCases']
  )
  @pytest_cases.parametrize_with_cases(
      'item_',
      cases='case_item.case_item',
      has_tag=['Well-Formed'],
      prefix=('weapon_', 'generated_item_', 'item_'),  # type: ignore
  )  # type: ignore
  def tuple_inventory_item_type(self, item_):
    validated_item = pydantic.TypeAdapter(
        item.Weapon | item.GeneratedItem | item.Item
    ).validate_python(item_)
    return item_, type(validated_item)


class PydanticDumpArgumentsCase:

  @pytest_cases.case(tags=['Well-Formed', 'ModelDumpJson'])
  def indent_4(self):
    return 4

  @pytest_cases.case(tags=['Well-Formed', 'ModelDumpJson'])
  def indent_none(self):
    return None

  @pytest_cases.case(tags=['Well-Formed', 'ModelDumpJson'])
  def include_none(self):
    return None

  @pytest_cases.case(tags=['Exclude', 'Well-Formed', 'ModelDumpJson'])
  def exclude_none(self):
    return None

  @pytest_cases.case(tags=['Well-Formed', 'ModelDumpJson'])
  @pytest_cases.parametrize('by_alias', [True, False])
  def by_alias_all(self, by_alias):
    return by_alias

  @pytest_cases.case(tags=['Well-Formed', 'ModelDumpJson'])
  @pytest_cases.parametrize('exclude_unset', [True, False])
  def exclude_unset_all(self, exclude_unset):
    return exclude_unset

  @pytest_cases.case(tags=['Well-Formed', 'ModelDumpJson'])
  @pytest_cases.parametrize('exclude_defaults', [True, False])
  def exclude_defaults_all(self, exclude_defaults):
    return exclude_defaults

  @pytest_cases.case(tags=['ExcludeNone', 'Well-Formed', 'ModelDumpJson'])
  @pytest_cases.parametrize('exclude_none', [True, False])
  def exclude_none_all(self, exclude_none):
    return exclude_none

  @pytest_cases.case(tags=['Well-Formed', 'ModelDumpJson'])
  @pytest_cases.parametrize('round_trip', [True, False])
  def round_trip_all(self, round_trip):
    return round_trip

  @pytest_cases.case(tags=['Well-Formed', 'ModelDumpJson'])
  @pytest_cases.parametrize('warnings', [True, False])
  def warnings_all(self, warnings):
    return warnings


@pytest_cases.parametrize_with_cases('indent', cases='.', prefix='indent_')
@pytest_cases.parametrize_with_cases('include', cases='.', prefix='include_')
@pytest_cases.parametrize_with_cases(
    'exclude', cases='.', has_tag=['Exclude'], prefix='exclude_'
)
@pytest_cases.parametrize_with_cases('by_alias', cases='.', prefix='by_alias_')
@pytest_cases.parametrize_with_cases(
    'exclude_unset', cases='.', prefix='exclude_unset_'
)
@pytest_cases.parametrize_with_cases(
    'exclude_defaults', cases='.', prefix='exclude_defaults_'
)
@pytest_cases.parametrize_with_cases(
    'exclude_none', cases='.', has_tag=['ExcludeNone'], prefix='exclude_none_'
)
@pytest_cases.parametrize_with_cases(
    'round_trip', cases='.', prefix='round_trip_'
)
@pytest_cases.parametrize_with_cases('warnings', cases='.', prefix='warnings_')
def pydantic_dump_arguments_well_formed(
    indent,
    include,
    exclude,
    by_alias,
    exclude_unset,
    exclude_defaults,
    exclude_none,
    round_trip,
    warnings,
):
  return {
      'indent': indent,
      'include': include,
      'exclude': exclude,
      'by_alias': by_alias,
      'exclude_unset': exclude_unset,
      'exclude_defaults': exclude_defaults,
      'exclude_none': exclude_none,
      'round_trip': round_trip,
      'warnings': warnings,
  }
