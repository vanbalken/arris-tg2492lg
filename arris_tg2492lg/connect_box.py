from __future__ import annotations

import base64
import json
import logging
import random

from aiohttp import ClientSession
from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional
from yarl import URL

from .const import HARDWARE_VERSION_OID, MAC_ADDRESS_OID, SERIAL_NUMBER_OID, SOFTWARE_VERSION_OID, USERNAME, TOKEN_EXPIRY_TIME
from .device import Device
from .mib_mapper import format_mac, to_devices

_LOGGER = logging.getLogger(__name__)


class ConnectBox:
    def __init__(self, websession: ClientSession, hostname: str, password: str):
        self.websession = websession
        self.hostname = hostname
        self.password = password
        self.nonce = str(random.randrange(10000, 100000))
        self.credential: Optional[Credential] = None

    async def async_get_credential(self) -> Credential:
        if self.credential is None or self.credential.expiration_time <= datetime.now().timestamp():
            token = await self.async_login()
            self.credential = Credential(token, datetime.now().timestamp() + TOKEN_EXPIRY_TIME)

        return self.credential

    async def async_login(self) -> str:
        arg_string = f"{USERNAME}:{self.password}"
        arg = base64.b64encode(arg_string.encode("utf-8")).decode("ascii")

        params = {"arg": arg, "_n": self.nonce}
        async with self.websession.get(f"{self.hostname}/login", params=params) as response:
            response.raise_for_status()

            token = await response.text()

            _LOGGER.debug("Received token: %s", token)

            return token

    async def async_logout(self) -> None:
        credential = await self.async_get_credential()

        params = {"_n": self.nonce}
        cookies = {"credential": credential.token}

        async with self.websession.get(f"{self.hostname}/logout", params=params, cookies=cookies) as response:
            if response.status != 500:
                response.raise_for_status()
            self.credential = None

    async def async_get_connected_devices(self, retry_on_unauthorized=True) -> List[Device]:
        credential = await self.async_get_credential()

        params = {"_n": self.nonce}
        cookies = {"credential": credential.token}
        async with self.websession.get(f"{self.hostname}/getConnDevices", params=params, cookies=cookies) as response:
            if retry_on_unauthorized is True and response.status == 401:
                self.credential = None
                return await self.async_get_connected_devices(False)

            response.raise_for_status()

            response_text = await response.text()

            _LOGGER.debug("getConnDevices response: %s", response.text)

            return to_devices(response_text)

    async def async_get_router_information(self) -> RouterInformation:
        oids = [
            MAC_ADDRESS_OID,
            HARDWARE_VERSION_OID,
            SOFTWARE_VERSION_OID,
            SERIAL_NUMBER_OID,
        ]

        snmp_get_result = await self._async_snmp_get(oids)

        router_information = RouterInformation(
            format_mac(snmp_get_result[MAC_ADDRESS_OID]).upper(),
            snmp_get_result[HARDWARE_VERSION_OID],
            snmp_get_result[SOFTWARE_VERSION_OID],
            snmp_get_result[SERIAL_NUMBER_OID])
        return router_information

    async def _async_snmp_get(self, oids: List[str]) -> Any:
        credential = await self.async_get_credential()

        # Manually create url because otherwise the semicolons are url encoded
        oids_joined = ";".join(oids)
        url = f"{self.hostname}/snmpGet?oids={oids_joined}&_n={self.nonce}"
        cookies = {"credential": credential.token}

        _LOGGER.debug("Get SNMP query %s results for router %s", oids, self.hostname)
        async with self.websession.get(URL(url), cookies=cookies) as response:
            _LOGGER.debug("url: %s", response.url)
            response.raise_for_status()

            data = await response.text()

            if data.startswith("Error"):
                _LOGGER.error("Error: %s, for url: %s", data, response.url)
                raise Exception(data)

            _LOGGER.debug("snmpGet response: %s", data)

            return json.loads(data)


@dataclass
class Credential:
    token: str
    expiration_time: float


@dataclass
class RouterInformation:
    mac_address: str
    hardware_version: str
    software_version: str
    serial_number: str
