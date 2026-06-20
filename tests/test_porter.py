import os
import pytest
from unittest.mock import patch, MagicMock

# Assuming resource_path is a context manager, we need to mock it properly
from alenia_porter.porter import get_ffmpeg_path

def test_get_ffmpeg_path_posix(mocker):
    """Test get_ffmpeg_path on non-Windows systems."""
    mocker.patch("alenia_porter.porter.os.name", "posix")

    assert get_ffmpeg_path() == "ffmpeg"


def test_get_ffmpeg_path_nt_exists_lower(mocker):
    """Test get_ffmpeg_path on Windows when ffmpeg.exe exists."""
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
    """Test get_ffmpeg_path on Windows when only ffmpeg.EXE exists."""
    mocker.patch("alenia_porter.porter.os.name", "nt")

    mock_resource_path = mocker.patch("alenia_porter.porter.resource_path")
    mock_context_manager1 = MagicMock()
    mock_context_manager2 = MagicMock()
    mock_resource_path.side_effect = [mock_context_manager1, mock_context_manager2]

    mock_context_manager1.__enter__.return_value = "C:\\path\\to\\bin\\ffmpeg.exe"
    mock_context_manager2.__enter__.return_value = "C:\\path\\to\\bin\\ffmpeg.EXE"

    mock_path_exists = mocker.patch("alenia_porter.porter.os.path.exists")
    # First call (ffmpeg.exe) is False, second call (ffmpeg.EXE) is True
    mock_path_exists.side_effect = [False, True]

    result = get_ffmpeg_path()

    assert result == "C:\\path\\to\\bin\\ffmpeg.EXE"
    assert mock_path_exists.call_count == 2
    mock_path_exists.assert_any_call("C:\\path\\to\\bin\\ffmpeg.exe")
    mock_path_exists.assert_any_call("C:\\path\\to\\bin\\ffmpeg.EXE")


def test_get_ffmpeg_path_nt_not_exists(mocker):
    """Test get_ffmpeg_path on Windows when neither ffmpeg.exe nor ffmpeg.EXE exists."""
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
