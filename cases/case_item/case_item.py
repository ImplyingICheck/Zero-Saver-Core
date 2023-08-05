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
import pytest_cases


@pytest_cases.parametrize(
    'value', [
        None, '', 'foo', {}, {
            'foo': 'bar'
        }, [], ['bar'], (), ('foo', 'bar'),
        object()
    ],
    ids=[
        'None', 'empty_string', '', 'empty_dict', '', 'empty_list', '',
        'empty_tuple', '', 'object()'
    ])
def any_value_potential_value(value):
  return value


class ItemCase:

  @pytest_cases.case(tags=['Item', 'Well-Formed'])
  def item_backpack9(self):
    return {
        'item': 'backpack9',
        'x': 248.0,
        'rotation': 0.0,
        'y': 119.0,
        'quantity': 1.0
    }


class GeneratedItemCase:

  @pytest_cases.case(tags=['GeneratedItem', 'Well-Formed'])
  def generated_item_bread(self):
    return {
        'x': 57.0,
        'rotation': 0.0,
        'y': 79.0,
        'durability': 100.0,
        'seen': 1.0,
        'created_from_player': 1.0,
        'item': 'bread',
        'quantity': 1.0
    }
