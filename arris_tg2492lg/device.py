from typing import Optional


class Device:
    def __init__(self, ip: str) -> None:
        self.ip = ip
        self.hostname: Optional[str] = None
        self.mac: Optional[str] = None
        self.adapter_type: Optional[str] = None
        self.type: Optional[str] = None
        self.lease_end: Optional[str] = None
        self.row_status: Optional[str] = None
        self.online: Optional[bool] = None
        self.comment: Optional[str] = None
        self.device_name: Optional[str] = None

    def __str__(self):
        return "ip: %s, hostname: %s" % (self.ip, self.hostname)
