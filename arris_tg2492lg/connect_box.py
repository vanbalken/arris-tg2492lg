from __future__ import annotations

import base64
import logging
import random

from aiohttp import ClientSession
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from .const import USERNAME, TOKEN_EXPIRY_TIME
from .device import Device
from .mib_mapper import to_devices

LOG = logging.getLogger(__name__)


class ConnectBox:
    def __init__(self, websession: ClientSession, hostname: str, password: str):
        self.websession = websession
        self.hostname = hostname
        self.password = password
        self.nonce = str(random.randrange(10000, 100000))
        self.credential: Optional[Credential] = None

    async def async_get_credential(self) -> Credential:
        if self.credential is None or self.credential.expiration_time >= datetime.now().timestamp():
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

            LOG.debug("Received token: %s", token)

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

            LOG.debug("getConnDevices response: %s", response.text)

            return to_devices(response_text)


@dataclass
class Credential:
    token: str
    expiration_time: float
