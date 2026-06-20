import os
import pytest
from unittest.mock import patch, mock_open

from alenia_porter.porter import load_dotenv

def test_load_dotenv_no_file():
    # Test when no .env file is found
    with patch("os.path.exists", return_value=False):
        with patch.dict(os.environ, {}, clear=True):
            load_dotenv()
            # os.environ should be empty (since we cleared it)
            assert len(os.environ) == 0

def test_load_dotenv_with_file():
    # Test reading valid key-value pairs, ignoring empty lines and comments
    mock_env_content = """
# This is a comment

KEY1=value1
KEY2 = value2
   KEY3= value3
"""
    with patch("os.path.exists", side_effect=lambda p: p.endswith(".env")):
        with patch("builtins.open", mock_open(read_data=mock_env_content)):
            with patch.dict(os.environ, {}, clear=True):
                load_dotenv()
                assert os.environ.get("KEY1") == "value1"
                assert os.environ.get("KEY2") == "value2"
                assert os.environ.get("KEY3") == "value3"
                assert len(os.environ) == 3

def test_load_dotenv_with_postgresql():
    # Test parsing postgresql URL correctly
    mock_env_content = """
postgresql://user:pass@localhost:5432/dbname
KEY1=val1
"""
    with patch("os.path.exists", side_effect=lambda p: p.endswith(".env")):
        with patch("builtins.open", mock_open(read_data=mock_env_content)):
            with patch.dict(os.environ, {}, clear=True):
                load_dotenv()
                assert os.environ.get("DATABASE_URL") == "postgresql://user:pass@localhost:5432/dbname"
                assert os.environ.get("KEY1") == "val1"
                assert len(os.environ) == 2

def test_load_dotenv_open_exception():
    # Test if open throws an exception
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", side_effect=Exception("Read error")):
            with patch.dict(os.environ, {}, clear=True):
                load_dotenv()
                # Should silently pass and not populate environment
                assert len(os.environ) == 0
