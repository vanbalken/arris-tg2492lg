import os
import pytest

from pathlib import Path
from requests import HTTPError

from arris_tg2492lg.connect_box import ConnectBox


def test_get_connected_devices(requests_mock):
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))
    test_data_path = current_path / "getConnDevices-response.json"
    get_conn_devices_json = test_data_path.read_text()

    requests_mock.get('/login', text="dummy_token")
    requests_mock.get('/getConnDevices', text=get_conn_devices_json)

    connect_box = ConnectBox("http://example.com", "secret")
    connected_devices = connect_box.get_connected_devices()

    assert len(connected_devices) == 4


def test_get_connected_devices_throws_401(requests_mock):
    requests_mock.get('/login', text="dummy_token")
    requests_mock.get('/getConnDevices', status_code=401)

    connect_box = ConnectBox("http://example.com", "secret")

    with pytest.raises(HTTPError):
        connect_box.get_connected_devices()
