from __future__ import annotations

import base64
import logging
import random
import requests
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from .const import USERNAME, TOKEN_EXPIRY_TIME
from .device import Device
from .mib_mapper import to_devices

LOG = logging.getLogger(__name__)


class ConnectBox:
    def __init__(self, hostname: str, password: str):
        self.hostname = hostname
        self.password = password
        self.nonce = str(random.randrange(10000, 100000))
        self.credential: Optional[Credential] = None

    def get_credential(self) -> Credential:
        if self.credential is None or self.credential.expiration_time >= datetime.now().timestamp():
            token = self.login()
            self.credential = Credential(token, datetime.now().timestamp() + TOKEN_EXPIRY_TIME)

        return self.credential

    def login(self) -> str:
        arg_string = f"{USERNAME}:{self.password}"
        arg = base64.b64encode(arg_string.encode("utf-8")).decode("ascii")

        params = {"arg": arg, "_n": self.nonce}
        response = requests.get(f"{self.hostname}/login", params=params)

        response.raise_for_status()

        if not response.text:
            raise Exception("Failed to login")

        token = response.text

        LOG.debug("Received token: %s", token)

        return token

    def logout(self):
        credential = self.get_credential()

        params = {"_n": self.nonce}
        cookies = {"credential": credential.token}
        response = requests.get(f"{self.hostname}/logout", params=params, cookies=cookies)

        # The router returns 500 INTERNAL_SERVER_ERROR on logout
        if response.status_code != 500:
            response.raise_for_status()

    def get_connected_devices(self) -> List[Device]:
        response = self.__call_get_connected_devices()

        if response.status_code == 401:
            self.credential = None
            response = self.__call_get_connected_devices()

        response.raise_for_status()

        LOG.debug("getConnDevices response: %s", response.text)

        return to_devices(response.text)

    def __call_get_connected_devices(self) -> requests.Response:
        credential = self.get_credential()

        params = {"_n": self.nonce}
        cookies = {"credential": credential.token}

        return requests.get(f"{self.hostname}/getConnDevices", params=params, cookies=cookies)


@dataclass
class Credential:
    token: str
    expiration_time: float
