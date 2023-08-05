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
import cmath
import decimal

import pytest_cases


@pytest_cases.parametrize(
    'value', [
        0, 1, None, '', 'foo', {}, {
            'foo': 'bar'
        }, [], ['bar'], (), ('foo', 'bar'),
        object()
    ],
    ids=[
        '0', '1', 'None', 'empty_string', 'non_empty_string', 'empty_dict',
        'non_empty_dict', 'empty_list', 'non_empty_list', 'empty_tuple',
        'non_empty_tuple', 'object()'
    ])
def any_value_potential_value(value):
  return value


@pytest_cases.case(tags=['CastableToInt', 'Well-Formed'])
@pytest_cases.parametrize('value', [
    '0', '1', 1, 0,
    decimal.Decimal(1),
    decimal.Decimal(1.0), 0.0, 1.0, b'0', b'1'
])
def castable_to_int_well_formed(value):
  return value


class CastableToIntCase:

  @pytest_cases.case(tags=['CastableToInt', 'Malformed', 'ValueError'])
  @pytest_cases.parametrize(
      'value', ['', 'Hello world!', b'', b'Hello world!'],
      ids=['empty_string', 'Hello world!', 'empty_bytes', 'Hello world!_bytes'])
  def castable_to_int_malformed_valueerror(self, value):
    return value

  @pytest_cases.case(tags=['CastableToInt', 'Malformed', 'OverflowError'])
  @pytest_cases.parametrize(
      'value', [cmath.inf, -cmath.inf],
      ids=['positive_infinity', 'negative_infinity'])
  def castable_to_int_malformed_overflowerror(self, value):
    return value

  @pytest_cases.case(tags=['CastableToInt', 'Malformed', 'TypeError'])
  @pytest_cases.parametrize('value', [object()], ids=['object()'])
  def castable_to_int_malformed_typeerror(self, value):
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


class WeaponCase:

  @pytest_cases.case(tags=['Weapon', 'Well-Formed', 'NoItemMods'])
  def weapon_akm_empty_mods(self):
    return {
        'x': 208.385650634765625,
        'rotation': 0.0,
        'seen': 1.0,
        'created_from_player': 0.0,
        'quantity': 1.0,
        'y': 30.54736328125,
        'durability': 91.507999999997849727151333354414,
        'ammo_id': 'ammo_762x39_hp',
        'ammo_quantity': 0.0,
        'item': 'akm',
        'weapon_fire_mode': 'automatic',
        'mods': {
            'magazine': 'no_item',
            'stock': 'no_item',
            'handguard': 'no_item',
            'brake': 'no_item',
            'att_2': 'no_item',
            'scope': 'no_item',
            'att_4': 'no_item',
            'grip': 'no_item',
            'barrel': 'no_item',
            'att_1': 'no_item',
            'att_3': 'no_item'
        }
    }

  @pytest_cases.case(tags=['Weapon', 'Well-Formed', 'NoneMods'])
  def weapon_akm_none_mods(self):
    return {
        'x': 208.385650634765625,
        'rotation': 0.0,
        'seen': 1.0,
        'created_from_player': 0.0,
        'quantity': 1.0,
        'y': 30.54736328125,
        'durability': 91.507999999997849727151333354414,
        'ammo_id': 'ammo_762x39_hp',
        'ammo_quantity': 0.0,
        'item': 'akm',
        'weapon_fire_mode': 'automatic',
        'mods': None
    }


class AttachmentsCase:

  @pytest_cases.case(tags=['Attachments', 'Well-Formed', 'NoItem'])
  def attachments_all_no_item(self):
    return {
        'magazine': 'no_item',
        'stock': 'no_item',
        'handguard': 'no_item',
        'brake': 'no_item',
        'att_2': 'no_item',
        'scope': 'no_item',
        'att_4': 'no_item',
        'grip': 'no_item',
        'barrel': 'no_item',
        'att_1': 'no_item',
        'att_3': 'no_item'
    }
