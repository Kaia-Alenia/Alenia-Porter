import os
import pytest
from unittest.mock import patch, MagicMock, mock_open
from alenia_porter.porter import get_ffmpeg_path, log_error_to_file

def test_get_ffmpeg_path_posix(mocker):
    mocker.patch("alenia_porter.porter.os.name", "posix")
    assert get_ffmpeg_path() == "ffmpeg"

def test_get_ffmpeg_path_nt_exists_lower(mocker):
    mocker.patch("alenia_porter.porter.os.name", "nt")
    mock_resource_path = mocker.patch("alenia_porter.porter.resource_path")
    mock_context_manager = MagicMock()
    mock_resource_path.return_value = mock_context_manager
    mock_context_manager.__enter__.return_value = "C:\\path\\to\\bin\\ffmpeg.exe"
    mock_path_exists = mocker.patch("alenia_porter.porter.os.path.exists")
    mock_path_exists.return_value = True
    result = get_ffmpeg_path()
    assert result == "C:\\path\\to\\bin\\ffmpeg.exe"
    mock_path_exists.assert_called_once_with("C:\\path\\to\\bin\\ffmpeg.exe")

def test_get_ffmpeg_path_nt_exists_upper(mocker):
    mocker.patch("alenia_porter.porter.os.name", "nt")
    mock_resource_path = mocker.patch("alenia_porter.porter.resource_path")
    mock_context_manager1 = MagicMock()
    mock_context_manager2 = MagicMock()
    mock_resource_path.side_effect = [mock_context_manager1, mock_context_manager2]
    mock_context_manager1.__enter__.return_value = "C:\\path\\to\\bin\\ffmpeg.exe"
    mock_context_manager2.__enter__.return_value = "C:\\path\\to\\bin\\ffmpeg.EXE"
    mock_path_exists = mocker.patch("alenia_porter.porter.os.path.exists")
    mock_path_exists.side_effect = [False, True]
    result = get_ffmpeg_path()
    assert result == "C:\\path\\to\\bin\\ffmpeg.EXE"
    assert mock_path_exists.call_count == 2
    mock_path_exists.assert_any_call("C:\\path\\to\\bin\\ffmpeg.exe")
    mock_path_exists.assert_any_call("C:\\path\\to\\bin\\ffmpeg.EXE")

def test_get_ffmpeg_path_nt_not_exists(mocker):
    mocker.patch("alenia_porter.porter.os.name", "nt")
    mock_resource_path = mocker.patch("alenia_porter.porter.resource_path")
    mock_context_manager1 = MagicMock()
    mock_context_manager2 = MagicMock()
    mock_resource_path.side_effect = [mock_context_manager1, mock_context_manager2]
    mock_context_manager1.__enter__.return_value = "C:\\path\\to\\bin\\ffmpeg.exe"
    mock_context_manager2.__enter__.return_value = "C:\\path\\to\\bin\\ffmpeg.EXE"
    mock_path_exists = mocker.patch("alenia_porter.porter.os.path.exists")
    mock_path_exists.return_value = False
    result = get_ffmpeg_path()
    assert result == "ffmpeg.exe"
    assert mock_path_exists.call_count == 2

def test_log_error_to_file_success():
    with patch("builtins.open", mock_open()) as mocked_file:
        log_error_to_file("Test error message")
        mocked_file.assert_called_once_with("ALENIA_ERROR.txt", "a", encoding="utf-8")
        mocked_file().write.assert_called_once_with("\n--- ERROR ---\nTest error message\n")

def test_log_error_to_file_exception():
    with patch("builtins.open", mock_open()) as mocked_file:
        mocked_file.side_effect = IOError("Mocked IO Error")
        log_error_to_file("This error cannot be written")
        mocked_file.assert_called_once_with("ALENIA_ERROR.txt", "a", encoding="utf-8")
