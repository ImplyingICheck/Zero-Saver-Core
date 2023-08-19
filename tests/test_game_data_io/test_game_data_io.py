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
import pydantic
import pytest
import pytest_cases
import pytest_mock

from zero_saver import game_data_io
from zero_saver.save_golden_files import typed_dict_0_31_production

_CASES = 'case_game_data_io.case_game_data_io'


@pytest.fixture
def mocked_save(mocker: pytest_mock.MockFixture):
  # pylint: disable=unnecessary-lambda
  save = mocker.MagicMock(spec=typed_dict_0_31_production.Model, name='save')
  save.configure_mock(
      __getitem__=lambda self, x: getattr(self, x),
      save_version='0.31 production')
  return save


@pytest.fixture
def mocked_game_data_io(mocker, mocked_save):
  mocker.patch('builtins.open')
  mocker.patch('zero_saver.game_data_io.FileLocation')
  mocker.patch.object(
      game_data_io.GameDataIO, '_read_save_file', return_value=mocked_save)
  return game_data_io.GameDataIO()


@pytest_cases.fixture
@pytest_cases.parametrize_with_cases(
    'save_file',
    cases=_CASES,
    prefix='save_file_path_',
    has_tag=['Well-Formed'])
def game_data_io_fixture(mocker, save_file):
  mocker.patch('zero_saver.game_data_io.FileLocation')
  return game_data_io.GameDataIO(save_file)


def test_game_data_io_verify_save_integrity_invalid_save_raises_validation_error(  # pylint: disable=line-too-long
    mocked_game_data_io):
  with pytest.raises(pydantic.ValidationError):
    mocked_game_data_io.verify_save_integrity()


def test_game_data_io_verify_save_integrity_invalid_save_version_raises_module_not_found_error(  # pylint: disable=line-too-long
    mocked_game_data_io):
  mocked_game_data_io.save.save_version = 'Unsupported save version'
  with pytest.raises(ModuleNotFoundError):
    mocked_game_data_io.verify_save_integrity()


def test_game_data_io_verify_save_integrity_missing_save_version_raises_key_error(  # pylint: disable=line-too-long
    mocked_game_data_io):
  mocked_game_data_io.save = {}
  with pytest.raises(KeyError):
    mocked_game_data_io.verify_save_integrity()


def test_game_data_io_verify_save_integrity_no_error_well_formed(
    game_data_io_fixture):
  game_data_io_fixture.verify_save_integrity()


def test_write_save_file_raises_value_error_invalid_save(mocked_game_data_io):
  with pytest.raises(ValueError):
    mocked_game_data_io.write_save_file()
