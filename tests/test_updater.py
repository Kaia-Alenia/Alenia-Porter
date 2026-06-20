import pytest
from unittest.mock import patch
from alenia_porter.updater import get_os_asset_name

def test_get_os_asset_name_windows():
    with patch('platform.system', return_value='Windows'):
        assert get_os_asset_name() == "AleniaPorter-Windows.zip"

def test_get_os_asset_name_mac():
    with patch('platform.system', return_value='Darwin'):
        assert get_os_asset_name() == "AleniaPorter-macOS.zip"

def test_get_os_asset_name_linux():
    with patch('platform.system', return_value='Linux'):
        assert get_os_asset_name() == "AleniaPorter-Linux.tar.gz"

def test_get_os_asset_name_fallback():
    with patch('platform.system', return_value='FreeBSD'):
        assert get_os_asset_name() == "AleniaPorter-Linux.tar.gz"
