import ipaddress
import os
import pytest

from pathlib import Path

from arris_tg2492lg.mib_mapper import format_date, format_mac, to_devices


def test_to_devices() -> None:
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))
    test_data_path = current_path / "getConnDevices-response.json"
    get_conn_devices_json = test_data_path.read_text()

    devices = to_devices(get_conn_devices_json)

    assert len(devices) == 4

    device = devices[0]

    assert device.ip == ipaddress.ip_address("192.168.178.2")
    assert device.hostname == "My Device"
    assert device.mac == "12:34:56:78:90:AB"
    assert device.adapter_type == "wireless1"
    assert device.type == "1"
    assert device.lease_end == "2019-11-03 16:51:04:00"
    assert device.row_status == "1"
    assert device.online
    assert device.comment == ""
    assert device.device_name == "unknown device"

    device2 = devices[1]

    assert device2.ip == ipaddress.ip_address("192.168.178.3")
    assert device2.hostname == "My Device 2"
    assert device2.mac == "BA:09:87:65:43:21"
    assert device2.adapter_type == "ethernet2"
    assert device2.type == "5"
    assert device2.lease_end == "0000-00-00 00:00:00:00"
    assert device2.row_status == "1"
    assert device2.online
    assert device2.comment == ""
    assert device2.device_name == "unknown device"

    device3 = devices[2]

    assert device3.ip == ipaddress.ip_address("2001:1c12:8d6:bb00:b0f6:855a:dcd:5528")
    assert device3.hostname == "My Device 3"
    assert device3.mac == "AA:AA:AA:AA:AA:AA"
    assert device3.adapter_type == "ethernet2"
    assert device3.type == "5"
    assert device3.lease_end == "0000-00-00 00:00:00:00"
    assert device3.row_status == "1"
    assert device3.online
    assert device3.comment == ""
    assert device3.device_name == "device 3"

    device4 = devices[3]

    assert device4.ip == ipaddress.ip_address("2001:1c12:8d6:bb00:b0f6:855a:dcd:5529")
    assert device4.hostname == "My Device"
    assert device4.mac == "12:34:56:78:90:AB"
    assert device4.adapter_type == "wireless1"
    assert device4.type == "1"
    assert device4.lease_end == "2019-11-03 16:51:04:00"
    assert device4.row_status == "1"
    assert device4.online
    assert device4.comment == ""
    assert device4.device_name == "unknown device"


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
