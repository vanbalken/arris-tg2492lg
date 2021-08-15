from arris_tg2492lg.const import CLIENT_ADAPTER_TYPE_OID, CLIENT_COMMENT_OID, CLIENT_DEVICE_NAME_OID, CLIENT_HOST_NAME_OID, CLIENT_LEASE_END_OID, CLIENT_MAC_OID, CLIENT_ONLINE_OID, CLIENT_ROW_STATUS_OID, CLIENT_TYPE_OID
import ipaddress
import json
import logging
import re
from collections import OrderedDict
from typing import List

from .device import Device

_LOGGER = logging.getLogger(__name__)

ADAPTER_TYPES = {
    0: "unknown",
    1: "ethernet",
    2: "usb",
    3: "moca",
    4: "dsg",
    5: "wireless1",
    6: "wireless2",
    7: "wireless3",
    8: "wireless4",
    9: "wireless5",
    10: "wireless6",
    11: "wireless7",
    12: "wireless8",
    13: "wireless9",
    14: "wireless10",
    15: "wireless11",
    16: "wireless12",
    17: "wireless13",
    18: "wireless14",
    19: "wireless15",
    20: "wireless16",
    21: "ethernet2",
    22: "ethernet3",
    23: "ethernet4"
}


def to_devices(json_string: str) -> List[Device]:
    """ Maps JSON result from router to Devices. """
    json_data: OrderedDict[str, str] = json.loads(json_string, object_pairs_hook=OrderedDict)
    devices: List[Device] = []
    current_device = None

    for key, value in json_data.items():
        split_key = key.split(".")

        if len(split_key) < 19:
            _LOGGER.debug("Found non-OID key: %s, with value: %s", key, value)
            continue

        oid = ".".join(split_key[:16])

        # ip address, either ipv4 or ipv6. ip version is specified by "split_key[17:19]", which can be ignored.
        ip_split = split_key[19:]
        ip_bytes = bytes(map(int, ip_split))
        ip = ipaddress.ip_address(ip_bytes)

        if current_device is None or current_device.ip != ip:
            current_device = Device(ip)
            devices.append(current_device)

        if oid == CLIENT_HOST_NAME_OID:
            current_device.hostname = value
        elif oid == CLIENT_MAC_OID:
            current_device.mac = format_mac(value)
        elif oid == CLIENT_ADAPTER_TYPE_OID:
            current_device.adapter_type = ADAPTER_TYPES[int(value)]
        elif oid == CLIENT_TYPE_OID:
            current_device.type = value
        elif oid == CLIENT_LEASE_END_OID:
            current_device.lease_end = format_date(value)
        elif oid == CLIENT_ROW_STATUS_OID:
            current_device.row_status = value
        elif oid == CLIENT_ONLINE_OID:
            current_device.online = value == "1"
        elif oid == CLIENT_COMMENT_OID:
            current_device.comment = value
        elif oid == CLIENT_DEVICE_NAME_OID:
            current_device.device_name = value
        else:
            _LOGGER.warn("Unknown OID: %s", key)

    return devices


def format_mac(value: str) -> str:
    if not re.fullmatch(r'^\$[0-9A-Fa-f]{12}$', value):
        raise ValueError(f"Received invalid MAC value: {value}")

    value = value[1:]
    mac = ""

    for i in range(6):
        mac += value[i * 2:i * 2 + 2]
        if i + 1 < 6:
            mac += ":"

    return mac


def format_date(value: str) -> str:
    if not re.fullmatch(r'^\$[0-9A-Fa-f]+$', value):
        raise ValueError(f"Received invalid date value: {value}")

    hex_array = bytes.fromhex(value[1:])

    years = hex_array[0] * 256 + hex_array[1]
    months = hex_array[2]
    days = hex_array[3]

    hours = hex_array[4]
    minutes = hex_array[5]
    seconds = hex_array[6]
    micro_seconds = hex_array[7]

    date = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}:{:02d}".format(years, months, days, hours, minutes, seconds, micro_seconds)
    return date
