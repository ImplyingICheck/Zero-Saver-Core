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


class _TestComponents(pydantic.BaseModel):
  original_kwargs: dict[str, Any]


class PlayerTestComponents(player.Player, _TestComponents):
  pass


@pytest_cases.fixture
@pytest_cases.parametrize_with_cases(
    'player', cases=_CASES, has_tag=['Well-Formed'], prefix='player_')
def player_fixture(player):
  return PlayerTestComponents(**player, original_kwargs=player)


def test_player_init_well_formed(player_fixture):
  assert player_fixture


def test_player_position_matches_x_y_values(player_fixture):
  expected_x = player_fixture.x
  expected_y = player_fixture.y
  assert player_fixture.position == (expected_x, expected_y)
