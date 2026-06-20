import pytest
from unittest.mock import patch, mock_open
from alenia_porter.porter import log_error_to_file

def test_log_error_to_file_success():
    """Test that log_error_to_file writes properly when no exception occurs."""
    with patch("builtins.open", mock_open()) as mocked_file:
        log_error_to_file("Test error message")
        mocked_file.assert_called_once_with("ALENIA_ERROR.txt", "a", encoding="utf-8")
        mocked_file().write.assert_called_once_with("\n--- ERROR ---\nTest error message\n")

def test_log_error_to_file_exception():
    """Test that log_error_to_file silently swallows exceptions like IOError."""
    with patch("builtins.open", mock_open()) as mocked_file:
        mocked_file.side_effect = IOError("Mocked IO Error")
        # Function should swallow the exception without raising
        log_error_to_file("This error cannot be written")

        # Verify open was called
        mocked_file.assert_called_once_with("ALENIA_ERROR.txt", "a", encoding="utf-8")
