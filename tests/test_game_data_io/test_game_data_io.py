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
# pylint: disable=line-too-long
import pathlib
import re

import pydantic
import pytest
import pytest_cases
import pytest_mock

from zero_saver_core import game_data_io
from zero_saver_core.save_golden_files import typed_dict_0_31_production

_CASES = 'case_game_data_io.case_game_data_io'


def strip_white_space(string):
  pattern = re.compile(r'\s*')
  pattern.sub('', string)


@pytest.fixture
def mocked_save(mocker: pytest_mock.MockFixture):
  # pylint: disable=unnecessary-lambda
  save = mocker.MagicMock(spec=typed_dict_0_31_production.Model, name='save')
  save.configure_mock(
      __getitem__=lambda self, x: getattr(self, x),
      save_version='0.31 production',
  )
  return save


@pytest.fixture
def mocked_game_data_io(mocker, mocked_save):
  mocker.patch('os.fdopen')
  mocker.patch('zero_saver_core.game_data_io.FileLocation')
  mocker.patch.object(
      game_data_io.GameDataIO, '_read_save_file', return_value=mocked_save
  )
  return game_data_io.GameDataIO()


@pytest_cases.fixture
@pytest_cases.parametrize_with_cases(
    'save_file', cases=_CASES, prefix='save_file_path_', has_tag=['Well-Formed']
)
def game_data_io_fixture(mocker, save_file):
  mocker.patch('zero_saver_core.game_data_io.FileLocation')
  return game_data_io.GameDataIO(save_file), save_file


class TestGameDataIOSave:

  def test_game_data_io_verify_save_integrity_invalid_save_raises_validation_error(
      self, mocked_game_data_io
  ):
    with pytest.raises(pydantic.ValidationError):
      mocked_game_data_io.verify_save_integrity()

  def test_game_data_io_verify_save_integrity_invalid_save_version_raises_module_not_found_error(
      self, mocked_game_data_io
  ):
    mocked_game_data_io.save.save_version = 'Unsupported save version'
    with pytest.raises(ModuleNotFoundError):
      mocked_game_data_io.verify_save_integrity()

  def test_game_data_io_verify_save_integrity_missing_save_version_raises_key_error(
      self, mocked_game_data_io
  ):
    mocked_game_data_io.save = {}
    with pytest.raises(KeyError):
      mocked_game_data_io.verify_save_integrity()

  @pytest.mark.slow
  def test_game_data_io_verify_save_integrity_no_error_well_formed(
      self, game_data_io_fixture
  ):
    game_data_io_, save_file = game_data_io_fixture
    del save_file  # Unused
    game_data_io_.verify_save_integrity()

  def test_game_data_io_write_save_file_raises_value_error_invalid_save(
      self, mocked_game_data_io
  ):
    with pytest.raises(ValueError):
      mocked_game_data_io.write_save_file()

  def test_game_data_io_write_save_file_invalid_save_version_raises_runtime_error(
      self, mocked_game_data_io
  ):
    mocked_game_data_io.save.save_version = 'Unsupported save version'
    with pytest.raises(
        RuntimeError,
        match='Failed during set up of integrity check.',
    ):
      mocked_game_data_io.write_save_file()

  def test_game_data_io_write_save_file_missing_save_version_raises_runtime_error(
      self, mocked_game_data_io
  ):
    mocked_game_data_io.save = {}
    with pytest.raises(KeyError):
      mocked_game_data_io.verify_save_integrity()

  def test_game_data_io_write_save_file_failed_backup_raises_runtime_error(
      self, mocker, mocked_game_data_io
  ):
    mocker.patch.object(
        game_data_io.GameDataIO, '_backup_save_file', return_value=False
    )
    mocker.patch.object(game_data_io.GameDataIO, 'verify_save_integrity')
    with pytest.raises(
        RuntimeError,
        match=(
            'The SHA-256 hash of the written backup file and original save file'
            ' do not match.'
        ),
    ):
      mocked_game_data_io.write_save_file()

  @pytest.mark.slow
  def test_game_data_io_write_save_file_well_formed_passes_correct_arguments_to_atomic_write(
      self, mocker: pytest_mock.MockFixture, game_data_io_fixture
  ):
    mocker.patch.object(
        game_data_io.GameDataIO, '_backup_save_file', return_value=True
    )
    mocked_open = mocker.patch('zero_saver_core.game_data_io._atomic_write')
    game_data_io_, expected_save_path = game_data_io_fixture
    game_data_io_.write_save_file()
    mocked_open.assert_called_with(expected_save_path, 'w', encoding='utf-8')

  @pytest.mark.slow
  def test_game_data_io_write_save_file_well_formed_writes_to_file_stream(
      self, mocker: pytest_mock.MockFixture, game_data_io_fixture
  ):
    mocker.patch.object(
        game_data_io.GameDataIO, '_backup_save_file', return_value=True
    )
    mocked_open = mocker.patch(
        'zero_saver_core.game_data_io._atomic_write', mocker.mock_open()
    )
    game_data_io_, expected_save_path = game_data_io_fixture
    del expected_save_path  # Unused
    game_data_io_.write_save_file()
    mocked_open().write.assert_called()

  @pytest.mark.slow
  def test_game_data_io_write_save_file_well_formed_writes_expected_contents(
      self,
      mocker: pytest_mock.MockFixture,
      game_data_io_fixture,
      file_like_fixture,
  ):
    mocker.patch.object(
        game_data_io.GameDataIO, '_backup_save_file', return_value=True
    )
    mocker.patch(
        'zero_saver_core.game_data_io._atomic_write', file_like_fixture()
    )
    game_data_io_, expected_save_path = game_data_io_fixture
    game_data_io_.write_save_file()
    expected_data = pathlib.Path(expected_save_path).read_text(encoding='utf-8')
    file_like_fixture.go_to_start()
    actual_data = file_like_fixture.read()
    assert strip_white_space(actual_data) == strip_white_space(expected_data)
