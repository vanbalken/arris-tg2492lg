from enum import Enum
from typing import Optional


class Device:
    def __init__(self, ip: str) -> None:
        self.ip = ip
        self.hostname: Optional[str] = None
        self.mac: Optional[str] = None
        self.adapter_type: Optional[LanClientAdapterType] = None
        self.type: Optional[LanClientType] = None
        self.lease_end: Optional[str] = None
        self.row_status: Optional[str] = None
        self.online: Optional[bool] = None
        self.comment: Optional[str] = None
        self.device_name: Optional[str] = None

    def __str__(self) -> str:
        return "ip: %s, hostname: %s" % (self.ip, self.hostname)


class LanClientAdapterType(Enum):
    """The type of the adapter."""

    UNKNOWN = 0
    ETHERNET = 1
    USB = 2
    MOCA = 3
    DSG = 4
    WIRELESS1 = 5
    WIRELESS2 = 6
    WIRELESS3 = 7
    WIRELESS4 = 8
    WIRELESS5 = 9
    WIRELESS6 = 10
    WIRELESS7 = 11
    WIRELESS8 = 12
    WIRELESS9 = 13
    WIRELESS10 = 14
    WIRELESS11 = 15
    WIRELESS12 = 16
    WIRELESS13 = 17
    WIRELESS14 = 18
    WIRELESS15 = 19
    WIRELESS16 = 20
    ETHERNET2 = 21
    ETHERNET3 = 22
    ETHERNET4 = 23


class LanClientType(Enum):
    """Type of IP address."""

    UNKNOWN = 0  # No client should use this value
    DYNAMIC = 1  # The client IP address is in DHCPv6 or DHCPv6 lease file, but it don't configured as Reserved client on WebGUI
    STATIC = 5  # If the client is online, and we can't find the client information in  DHCPv4 or DHCPv6 lease file and it is not configured as Reserved client on WebGUI, then we put it types to static. Notice IPv6 stateless client and link local client would also tagged as this type
    DYNAMIC_RESERVED = 6  # The Reserved client configured on WebGUI
