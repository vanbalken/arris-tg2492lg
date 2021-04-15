import os
import pytest

from aiohttp import web
from pathlib import Path
from requests import HTTPError

from arris_tg2492lg.connect_box import ConnectBox


async def test_async_get_credential(aiohttp_client, loop):
    app = web.Application(loop=loop)
    app.router.add_get("/login", get_credential)
    client = await aiohttp_client(app)

    connect_box = ConnectBox(client.session, f"http://{client.host}:{client.port}", "secret")
    credential = await connect_box.async_get_credential()

    print(credential.token)

    assert credential.token == 'dummy_token'


async def test_get_connected_devices(aiohttp_client, loop):
    app = web.Application(loop=loop)
    app.router.add_get("/login", get_credential)
    app.router.add_get("/getConnDevices", get_mock_data)
    client = await aiohttp_client(app)

    connect_box = ConnectBox(client.session, f"http://{client.host}:{client.port}", "secret")
    connected_devices = await connect_box.async_get_connected_devices()

    assert len(connected_devices) == 4

    # TODO fix unit tests

    # assert login_adapter.call_count == 1
    # assert get_connected_devices_adapter.call_count == 1


# def test_get_connected_devices_throws_401_once(requests_mock):
#     get_conn_devices_json = get_mock_data()

#     login_adapter = requests_mock.get('/login', text="dummy_token")
#     get_connected_devices_adapter = requests_mock.get('/getConnDevices',
#                                                       [{"status_code": 401},
#                                                        {"text": get_conn_devices_json}])

#     connect_box = ConnectBox("http://example.com", "secret")
#     connected_devices = connect_box.get_connected_devices()

#     assert len(connected_devices) == 4

#     assert login_adapter.call_count == 2
#     assert get_connected_devices_adapter.call_count == 2


# def test_get_connected_devices_throws_401_twice(requests_mock):
#     login_adapter = requests_mock.get('/login', text="dummy_token")
#     get_connected_devices_adapter = requests_mock.get('/getConnDevices', status_code=401)

#     connect_box = ConnectBox("http://example.com", "secret")

#     with pytest.raises(HTTPError):
#         connect_box.get_connected_devices()

#     assert login_adapter.call_count == 2
#     assert get_connected_devices_adapter.call_count == 2

# def test_logout_accepts_http_status_500(requests_mock):
#     login_adapter = requests_mock.get('/login', text="dummy_token")
#     logout_adapter = requests_mock.get('/logout', status_code=500)

#     connect_box = ConnectBox("http://example.com", "secret")
#     connect_box.logout()

#     assert login_adapter.call_count == 1
#     assert logout_adapter.call_count == 1

# def test_logout_throws_for_401_unauthorized(requests_mock):
#     login_adapter = requests_mock.get('/login', text="dummy_token")
#     logout_adapter = requests_mock.get('/logout', status_code=401)

#     connect_box = ConnectBox("http://example.com", "secret")

#     with pytest.raises(HTTPError):
#         connect_box.logout()

#     assert login_adapter.call_count == 1
#     assert logout_adapter.call_count == 1

async def get_credential(request):
    return web.Response(text='dummy_token')

async def get_mock_data(request):
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))
    test_data_path = current_path / "getConnDevices-response.json"

    return web.Response(text=test_data_path.read_text())
