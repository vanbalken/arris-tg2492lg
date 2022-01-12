import os
import pytest

from pathlib import Path
from requests import HTTPError

from arris_tg2492lg.connect_box import ConnectBox


def test_login_url_replaces_special_characters_in_password(requests_mock):
    """Validates that special characters in the password are replaced.
    The webpage of the router replaces special characters in both the username and password using the '%xx' escape.
    """
    login_adapter = requests_mock.get("/login", text="dummy_token")
    requests_mock.get("/getConnDevices", text="{}")

    connect_box = ConnectBox("http://example.com", "&=")
    connect_box.get_connected_devices()

    assert login_adapter.call_count == 1
    assert login_adapter.request_history[0].url.startswith("http://example.com/login?arg=YWRtaW46JTI2JTNE&_n=")


def test_login_does_not_url_encode_base64(requests_mock):
    """Validate that the characters in the base64 arg parameter are not replaced.
    The portal of the router does not replace special characters (=) in the base64 encoded parameter.
    """
    login_adapter = requests_mock.get("/login", text="dummy_token")
    requests_mock.get("/getConnDevices", text="{}")

    connect_box = ConnectBox("http://example.com", "secret2")
    connect_box.get_connected_devices()

    assert login_adapter.call_count == 1
    assert login_adapter.request_history[0].url.startswith("http://example.com/login?arg=YWRtaW46c2VjcmV0Mg==&_n=")


def test_get_connected_devices(requests_mock):
    get_conn_devices_json = get_mock_data()

    login_adapter = requests_mock.get("/login", text="dummy_token")
    get_connected_devices_adapter = requests_mock.get("/getConnDevices", text=get_conn_devices_json)

    connect_box = ConnectBox("http://example.com", "secret")
    connected_devices = connect_box.get_connected_devices()

    assert len(connected_devices) == 4

    assert login_adapter.call_count == 1
    assert login_adapter.request_history[0].url.startswith("http://example.com/login?arg=YWRtaW46c2VjcmV0&_n=")
    assert get_connected_devices_adapter.call_count == 1


def test_get_connected_devices_throws_401_once(requests_mock):
    get_conn_devices_json = get_mock_data()

    login_adapter = requests_mock.get("/login", text="dummy_token")
    get_connected_devices_adapter = requests_mock.get("/getConnDevices",
                                                      [{"status_code": 401},
                                                       {"text": get_conn_devices_json}])

    connect_box = ConnectBox("http://example.com", "secret")
    connected_devices = connect_box.get_connected_devices()

    assert len(connected_devices) == 4

    assert login_adapter.call_count == 2
    assert get_connected_devices_adapter.call_count == 2


def test_get_connected_devices_throws_401_twice(requests_mock):
    login_adapter = requests_mock.get("/login", text="dummy_token")
    get_connected_devices_adapter = requests_mock.get("/getConnDevices", status_code=401)

    connect_box = ConnectBox("http://example.com", "secret")

    with pytest.raises(HTTPError):
        connect_box.get_connected_devices()

    assert login_adapter.call_count == 2
    assert get_connected_devices_adapter.call_count == 2


def test_logout_accepts_http_status_500(requests_mock):
    login_adapter = requests_mock.get("/login", text="dummy_token")
    logout_adapter = requests_mock.get("/logout", status_code=500)

    connect_box = ConnectBox("http://example.com", "secret")
    connect_box.logout()

    assert login_adapter.call_count == 1
    assert logout_adapter.call_count == 1


def test_logout_throws_for_401_unauthorized(requests_mock):
    login_adapter = requests_mock.get("/login", text="dummy_token")
    logout_adapter = requests_mock.get("/logout", status_code=401)

    connect_box = ConnectBox("http://example.com", "secret")

    with pytest.raises(HTTPError):
        connect_box.logout()

    assert login_adapter.call_count == 1
    assert logout_adapter.call_count == 1


def get_mock_data():
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))
    test_data_path = current_path / "getConnDevices-response.json"

    return test_data_path.read_text()
