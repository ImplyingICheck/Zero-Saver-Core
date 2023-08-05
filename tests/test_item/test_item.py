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


def test_item_init_well_formed(item_fixture):
  assert item_fixture


@pytest_cases.parametrize('expected_property',
                          ['item', 'x', 'y', 'quantity', 'rotation'])
def test_item_public_properties(item_fixture, expected_property):
  assert hasattr(item_fixture, expected_property)


def test_item_converts_quantity_to_int(item_fixture):
  expected_type = int
  actual_value = item_fixture.quantity
  assert isinstance(actual_value, expected_type)
