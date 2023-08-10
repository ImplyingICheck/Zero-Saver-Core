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
import pytest_cases.filters


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
        'thirst': 90.0
    }


class InventoryCase:

  @pytest_cases.case(tags=['Inventory', 'Well-Formed', 'ExternalCases'])
  @pytest_cases.parametrize_with_cases(
      'item',
      cases='case_item.case_item',
      has_tag=['Well-Formed'],
      prefix=('weapon_', 'generated_item_', 'item_'))
  def inventory_single_well_formed_item_cases(self, item):
    return {'items': [item]}
