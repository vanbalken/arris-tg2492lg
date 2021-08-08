import os
import pytest

from aiohttp import web, ClientResponseError
from pathlib import Path

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


async def test_get_connected_devices_throws_401_once(aiohttp_client, loop):
    def login_result(request):
        login_result.call_count += 1
        return get_credential(request)

    def conn_devices_result(request):
        conn_devices_result.call_count += 1
        if conn_devices_result.call_count == 1:
            return web.Response(status=401)
        else:
            return get_mock_data(request)

    login_result.call_count = 0
    conn_devices_result.call_count = 0

    app = web.Application(loop=loop)
    app.router.add_get("/login", login_result)
    app.router.add_get("/getConnDevices", conn_devices_result)
    client = await aiohttp_client(app)

    connect_box = ConnectBox(client.session, f"http://{client.host}:{client.port}", "secret")
    connected_devices = await connect_box.async_get_connected_devices()

    assert len(connected_devices) == 4

    assert login_result.call_count == 2
    assert conn_devices_result.call_count == 2


async def test_get_connected_devices_throws_401_twice(aiohttp_client, loop):
    def login_result(request):
        login_result.call_count += 1
        return get_credential(request)

    def conn_devices_result(request):
        conn_devices_result.call_count += 1
        return web.Response(status=401)

    login_result.call_count = 0
    conn_devices_result.call_count = 0

    app = web.Application(loop=loop)
    app.router.add_get("/login", login_result)
    app.router.add_get("/getConnDevices", conn_devices_result)
    client = await aiohttp_client(app)

    connect_box = ConnectBox(client.session, f"http://{client.host}:{client.port}", "secret")

    with pytest.raises(ClientResponseError):
        await connect_box.async_get_connected_devices()

    assert login_result.call_count == 2
    assert conn_devices_result.call_count == 2


async def test_logout_accepts_http_status_500(aiohttp_client, loop):
    def get_logout_success(request):
        get_logout_success.call_count += 1
        return web.Response(status=500)

    get_logout_success.call_count = 0

    app = web.Application(loop=loop)
    app.router.add_get("/login", get_credential)
    app.router.add_get("/logout", get_logout_success)
    client = await aiohttp_client(app)

    connect_box = ConnectBox(client.session, f"http://{client.host}:{client.port}", "secret")
    await connect_box.async_logout()

    assert get_logout_success.call_count == 1


async def test_logout_throws_for_401_unauthorized(aiohttp_client, loop):
    async def get_logout_failure(request):
        get_logout_failure.call_count += 1
        return web.Response(status=401)

    get_logout_failure.call_count = 0

    app = web.Application(loop=loop)
    app.router.add_get("/login", get_credential)
    app.router.add_get("/logout", get_logout_failure)
    client = await aiohttp_client(app)

    connect_box = ConnectBox(client.session, f"http://{client.host}:{client.port}", "secret")

    with pytest.raises(ClientResponseError):
        await connect_box.async_logout()

    assert get_logout_failure.call_count == 1


def get_credential(request):
    return web.Response(text='dummy_token')


def get_mock_data(request):
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))
    test_data_path = current_path / "getConnDevices-response.json"

    return web.Response(text=test_data_path.read_text())
