from __future__ import annotations

import base64
import json
import logging
import random

from aiohttp import ClientSession
from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional
from urllib.parse import quote
from yarl import URL

from .const import (
    HARDWARE_VERSION_OID,
    MAC_ADDRESS_OID,
    SERIAL_NUMBER_OID,
    SOFTWARE_VERSION_OID,
    TOKEN_EXPIRATION,
    USERNAME,
)
from .device import Device
from .exception import ConnectBoxError, InvalidCredentialError
from .mib_mapper import format_mac, to_devices

_LOGGER = logging.getLogger(__name__)


class ConnectBox:
    def __init__(self, websession: ClientSession, hostname: str, password: str):
        self._websession = websession
        self._hostname = hostname
        self._password = quote(password)
        self._nonce = str(random.randrange(10000, 100000))
        self._credential: Optional[Credential] = None

    async def async_login(self) -> str:
        arg_string = f"{USERNAME}:{self._password}"
        arg = base64.b64encode(arg_string.encode("utf-8")).decode("ascii")

        params = {"arg": arg, "_n": self._nonce}
        async with self._websession.get(f"{self._hostname}/login", params=params) as response:
            response.raise_for_status()

            token = await response.text()

            _LOGGER.debug("Received token: %s", token)

            self._credential = Credential(token)
            self._credential.validate()

            return token

    async def async_logout(self) -> None:
        credential = await self._async_get_credential()

        params = {"_n": self._nonce}
        cookies = {"credential": credential.token}

        async with self._websession.get(f"{self._hostname}/logout", params=params, cookies=cookies) as response:
            if response.status != 500:
                response.raise_for_status()
            self._credential = None

    async def async_get_connected_devices(self, retry_on_unauthorized=True) -> List[Device]:
        """Get all connected devices.

        A device is returned for every IP address. When a device has both a IPv4 and a IPv6 address it will appear
        twice in the returned list.
        """
        credential = await self._async_get_credential()

        params = {"_n": self._nonce}
        cookies = {"credential": credential.token}
        async with self._websession.get(f"{self._hostname}/getConnDevices", params=params, cookies=cookies) as response:
            if retry_on_unauthorized is True and response.status == 401:
                self._credential = None
                return await self.async_get_connected_devices(False)

            response.raise_for_status()

            response_text = await response.text()

            _LOGGER.debug("getConnDevices response: %s", response_text)

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
            format_mac(snmp_get_result[MAC_ADDRESS_OID]),
            snmp_get_result[HARDWARE_VERSION_OID],
            snmp_get_result[SOFTWARE_VERSION_OID],
            snmp_get_result[SERIAL_NUMBER_OID],
        )
        return router_information

    async def _async_get_credential(self) -> Credential:
        if self._credential is None or self._credential.is_expired():
            await self.async_login()

        return self._credential  # type: ignore

    async def _async_snmp_get(self, oids: List[str]) -> Any:
        credential = await self._async_get_credential()

        # Manually create url because otherwise the semicolons are url encoded.
        oids_joined = ";".join(oids)
        url = f"{self._hostname}/snmpGet?oids={oids_joined}&_n={self._nonce}"
        cookies = {"credential": credential.token}

        _LOGGER.debug("Get SNMP query %s results for router %s", oids, self._hostname)
        async with self._websession.get(URL(url), cookies=cookies) as response:
            response.raise_for_status()

            data = await response.text()

            # Response starts with "Error in OID formatting!" when an invalid OID is requested.
            if data.startswith("Error"):
                raise ConnectBoxError(data)

            _LOGGER.debug("snmpGet response: %s", data)

            return json.loads(data)


class Credential:
    def __init__(self, token: str):
        self._token = token
        self._created_at = datetime.now()

    def is_expired(self) -> bool:
        expires = self._created_at + TOKEN_EXPIRATION
        return datetime.now() > expires

    def validate(self) -> None:
        try:
            self._token_as_json()
        except Exception as exc:
            raise InvalidCredentialError from exc

    def is_multi_login(self) -> bool:
        """Return if the user is already logged in."""

        is_logged_in_value = self._is_logged_in()

        return is_logged_in_value > 0

    @property
    def token(self) -> str:
        return self._token

    def _is_logged_in(self) -> int:
        """Return if the user is already logged in.

        Reverse engineered from a javascript library of the routers web application. The response of this method doesn't
        indicate if a consecutive call will fail or succeed. Method is kept for reference.
        """
        token_json = self._token_as_json()

        if "muti" in token_json:
            muti = token_json["muti"]
            con_type = token_json["conType"]
            gw_wan = token_json["gwWan"]

            if gw_wan == "f" and con_type == "LAN" and muti == "GW_WAN":
                return 2  # Remote user already login.
            elif gw_wan == "t" and muti == "LAN":
                return 1  # Local user already login.
            if gw_wan == "f" and con_type == "LAN" and muti == "LAN":
                return 3  # Other local user already login.
            elif gw_wan == "t" and muti == "GW_WAN":
                return 4  # Other remote user already login.

        return 0

    def _token_as_json(self) -> Any:
        decoded_token = base64.b64decode(self._token)
        return json.loads(decoded_token)


@dataclass
class RouterInformation:
    mac_address: str
    hardware_version: str
    software_version: str
    serial_number: str
