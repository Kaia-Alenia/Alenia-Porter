import json
import urllib.request
import pytest
from alenia_porter.updater import check_for_updates

def test_check_for_updates_no_update_available(mocker):
    # Setup
    current_version = "v1.0.0"
    mock_response = mocker.MagicMock()
    # Read decode returns json string
    mock_response.read.return_value.decode.return_value = json.dumps({
        "tag_name": "v1.0.0"
    })
    
    mock_urlopen = mocker.patch('urllib.request.urlopen')
    # urlopen behaves as a context manager
    mock_urlopen.return_value.__enter__.return_value = mock_response

    # Execute
    result = check_for_updates(current_version)

    # Assert
    assert result == (False, None, None)

def test_check_for_updates_update_available(mocker):
    # Setup
    current_version = "v1.0.0"
    latest_version = "v1.1.0"
    target_asset = "AleniaPorter-Linux.tar.gz"
    download_url = "https://example.com/download.tar.gz"
    
    mock_response = mocker.MagicMock()
    mock_response.read.return_value.decode.return_value = json.dumps({
        "tag_name": latest_version,
        "assets": [
            {
                "name": target_asset,
                "browser_download_url": download_url
            }
        ]
    })
    
    mock_urlopen = mocker.patch('urllib.request.urlopen')
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    # Mock get_os_asset_name so test is platform independent
    mocker.patch('alenia_porter.updater.get_os_asset_name', return_value=target_asset)

    # Execute
    result = check_for_updates(current_version)

    # Assert
    assert result == (True, latest_version, download_url)

def test_check_for_updates_no_matching_asset(mocker):
    # Setup
    current_version = "v1.0.0"
    latest_version = "v1.1.0"
    
    mock_response = mocker.MagicMock()
    mock_response.read.return_value.decode.return_value = json.dumps({
        "tag_name": latest_version,
        "assets": [
            {
                "name": "Different-Asset.zip",
                "browser_download_url": "https://example.com/different.zip"
            }
        ]
    })
    
    mock_urlopen = mocker.patch('urllib.request.urlopen')
    mock_urlopen.return_value.__enter__.return_value = mock_response
    
    mocker.patch('alenia_porter.updater.get_os_asset_name', return_value="AleniaPorter-Linux.tar.gz")

    # Execute
    result = check_for_updates(current_version)

    # Assert
    assert result == (False, None, None)

def test_check_for_updates_network_error(mocker, capsys):
    # Setup
    current_version = "v1.0.0"
    
    mock_urlopen = mocker.patch('urllib.request.urlopen', side_effect=urllib.error.URLError("Network unreachable"))

    # Execute
    result = check_for_updates(current_version)

    # Assert
    assert result == (False, None, None)
    captured = capsys.readouterr()
    assert "Error checking for updates:" in captured.out
