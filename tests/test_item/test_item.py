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
