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

from zero_saver import item

_CASES = 'case_item.case_item'


class ItemTestComponents(item.Item):

  def __init__(self, *args, **kwargs):
    self.original_args = args
    self.original_kwargs = kwargs
    super().__init__(*args, **kwargs)


@pytest_cases.fixture
@pytest_cases.parametrize_with_cases(
    'item', has_tag=['Well-Formed'], cases=_CASES, prefix='item_')
def item_fixture(item):
  return ItemTestComponents(**item)


class TestItem:

  def test_item_init_well_formed(self, item_fixture):
    assert item_fixture

  @pytest_cases.parametrize('expected_property',
                            ['item', 'x', 'y', 'quantity', 'rotation'])
  def test_item_public_properties(self, item_fixture, expected_property):
    assert hasattr(item_fixture, expected_property)

  def test_item_converts_quantity_to_int(self, item_fixture):
    expected_type = int
    actual_value = item_fixture.quantity
    assert isinstance(actual_value, expected_type)

  def test_item_converts_rotation_to_bool(self, item_fixture):
    expected_type = bool
    actual_value = item_fixture.rotation
    assert isinstance(actual_value, expected_type)

  @pytest_cases.parametrize_with_cases(
      'item_dict', has_tag=['Well-Formed'], cases=_CASES, prefix='item_')
  @pytest_cases.parametrize_with_cases(
      'malformed_value',
      has_tag=['Malformed'],
      cases=_CASES,
      prefix='castable_to_int_')
  def test_item_raises_value_error_on_malformed_quantity(
      self, item_dict, malformed_value):
    item_dict['quantity'] = malformed_value
    with pytest.raises(ValueError):
      item.Item(**item_dict)


class GeneratedItemTestComponents(item.GeneratedItem):

  def __init__(self, *args, **kwargs):
    self.original_args = args
    self.original_kwargs = kwargs
    super().__init__(*args, **kwargs)


@pytest_cases.fixture
@pytest_cases.parametrize_with_cases(
    'generated_item',
    has_tag=['Well-Formed'],
    cases=_CASES,
    prefix='generated_item_')
def generated_item_fixture(generated_item):
  return GeneratedItemTestComponents(**generated_item)


class TestGeneratedItem:

  def test_generated_item_init_well_formed(self, generated_item_fixture):
    assert generated_item_fixture

  @pytest_cases.parametrize('expected_property', [
      'item', 'x', 'y', 'quantity', 'rotation', 'seen', 'durability',
      'created_from_player'
  ])
  def test_generated_item_public_properties(self, generated_item_fixture,
                                            expected_property):
    assert hasattr(generated_item_fixture, expected_property)

  def test_generated_item_converts_seen_to_bool(self, generated_item_fixture):
    expected_type = bool
    actual_value = generated_item_fixture.seen
    assert isinstance(actual_value, expected_type)

  def test_generated_item_converts_created_from_player_to_bool(
      self, generated_item_fixture):
    expected_type = bool
    actual_value = generated_item_fixture.created_from_player
    assert isinstance(actual_value, expected_type)


class TestParseFunctions:

  class TestParseBool:

    @pytest_cases.parametrize_with_cases(
        'value', cases=_CASES, prefix='any_value_')
    def test_parse_bool_returns_bool(self, value):
      return_value = item.parse_bool(value)
      assert isinstance(return_value, bool)

    @pytest_cases.parametrize_with_cases(
        'value', cases=_CASES, prefix='any_value_')
    def test_parse_bool_returns_correct_bool(self, value):
      expected_value = bool(value)
      return_value = item.parse_bool(value)
      assert return_value == expected_value

  class TestParseInt:

    @pytest_cases.parametrize_with_cases(
        'value',
        has_tag=['Well-Formed'],
        cases=_CASES,
        prefix='castable_to_int_')
    def test_parse_int_well_formed_returns_int(self, value):
      return_value = item.parse_int(value)
      assert isinstance(return_value, int)

    @pytest_cases.parametrize_with_cases(
        'value', has_tag=['Malformed'], cases=_CASES, prefix='castable_to_int_')
    def test_parse_int_malformed_raises_exception(self, value):
      with pytest.raises(Exception):
        item.parse_int(value)

    @pytest_cases.parametrize_with_cases(
        'value',
        has_tag=['Malformed', 'OverflowError'],
        cases=_CASES,
        prefix='castable_to_int_')
    def test_parse_int_large_numbers_raise_overflowerror(self, value):
      with pytest.raises(OverflowError):
        item.parse_int(value)

    @pytest_cases.parametrize_with_cases(
        'value',
        has_tag=['Malformed', 'TypeError'],
        cases=_CASES,
        prefix='castable_to_int_')
    def test_parse_int_incompatible_value_raises_value_error(self, value):
      with pytest.raises(TypeError):
        item.parse_int(value)
