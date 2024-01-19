import os
import pytest

from pathlib import Path
from arris_tg2492lg.device import LanClientAdapterType, LanClientType

from arris_tg2492lg.mib_mapper import format_date, format_mac, to_devices


def test_to_devices() -> None:
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))
    test_data_path = current_path / "getConnDevices-response.json"
    get_conn_devices_json = test_data_path.read_text()

    devices = to_devices(get_conn_devices_json)

    assert len(devices) == 4

    device = devices[0]

    assert device.ip == "192.168.178.2"
    assert device.hostname == "My Device"
    assert device.mac == "12:34:56:78:90:AB"
    assert device.adapter_type == LanClientAdapterType.WIRELESS1
    assert device.type == LanClientType.DYNAMIC
    assert device.lease_end == "2019-11-03 16:51:04:00"
    assert device.row_status == "1"
    assert device.online
    assert device.comment == ""
    assert device.device_name == "unknown device"

    device2 = devices[1]

    assert device2.ip == "192.168.178.3"
    assert device2.hostname == "My Device 2"
    assert device2.mac == "BA:09:87:65:43:21"
    assert device2.adapter_type == LanClientAdapterType.ETHERNET2
    assert device2.type == LanClientType.STATIC
    assert device2.lease_end == "0000-00-00 00:00:00:00"
    assert device2.row_status == "1"
    assert device2.online
    assert device2.comment == ""
    assert device2.device_name == "unknown device"

    device3 = devices[2]

    assert device3.ip == "2001:1c12:8d6:bb00:b0f6:855a:dcd:5528"
    assert device3.hostname == "My Device 3"
    assert device3.mac == "AA:AA:AA:AA:AA:AA"
    assert device3.adapter_type == LanClientAdapterType.ETHERNET2
    assert device3.type == LanClientType.STATIC
    assert device3.lease_end == "0000-00-00 00:00:00:00"
    assert device3.row_status == "1"
    assert device3.online
    assert device3.comment == ""
    assert device3.device_name == "device 3"

    device4 = devices[3]

    assert device4.ip == "2001:1c12:8d6:bb00:b0f6:855a:dcd:5529"
    assert device4.hostname == "My Device"
    assert device4.mac == "12:34:56:78:90:AB"
    assert device4.adapter_type == LanClientAdapterType.WIRELESS1
    assert device4.type == LanClientType.DYNAMIC
    assert device4.lease_end == "2019-11-03 16:51:04:00"
    assert device4.row_status == "1"
    assert device4.online
    assert device4.comment == ""
    assert device4.device_name == "unknown device"


def test_to_devices_with_invalid_lan_client_type():
    json = """
    {
        "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.3.200.1.4.192.168.178.2":"My Device",
        "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.4.200.1.4.192.168.178.2":"$1234567890AB",
        "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.6.200.1.4.192.168.178.2":"5",
        "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.7.200.1.4.192.168.178.2":"-1",
        "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.9.200.1.4.192.168.178.2":"$07e30b0310330400",
        "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.13.200.1.4.192.168.178.2":"1",
        "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.14.200.1.4.192.168.178.2":"1",
        "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.15.200.1.4.192.168.178.2":"",
        "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.20.200.1.4.192.168.178.2":"unknown device",
        "routerCurrentTime":"2020-01-09 21:40:21.00",
        "1": "Finish"
    }
    """

    with pytest.raises(ValueError):
        to_devices(json)


def test_format_mac_ok():
    result = format_mac("$1234567890ab")
    assert result == "12:34:56:78:90:ab"


def test_format_mac_error():
    with pytest.raises(ValueError):
        format_mac("invalid_value")


def test_format_date_ok():
    result = format_date("$07e30b0310330400")
    assert result == "2019-11-03 16:51:04:00"


def test_format_date_error():
    with pytest.raises(ValueError):
        format_date("invalid_value")
