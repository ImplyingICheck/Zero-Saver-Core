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


@pytest_cases.fixture
@pytest_cases.parametrize_with_cases(
    'stash_data', cases=_CASES, prefix='stash_', has_tag=['Well-Formed'])
def stash_fixture(stash_data):
  return stash.Stash(chests=stash_data)


def test_stash_init_well_formed(stash_fixture):
  assert stash_fixture
