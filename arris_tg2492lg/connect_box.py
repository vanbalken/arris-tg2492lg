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
        self.credentials: Optional[Credentials] = None

    def get_credentials(self) -> Credentials:
        if self.credentials is None or self.credentials.expiration_time >= datetime.now().timestamp():
            token = self.login()
            self.credentials = Credentials(token, datetime.now().timestamp() + TOKEN_EXPIRY_TIME)

        return self.credentials

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

    def logout(self) -> None:
        credentials = self.get_credentials()

        params = {"_n": self.nonce}
        cookies = {"credential": credentials.token}
        response = requests.get(f"{self.hostname}/logout", params=params, cookies=cookies)

        # The router returns 500 (Internal Server Error) on a successfull logout
        if response.status_code != 500:
            response.raise_for_status()

        self.credentials = None

    def get_connected_devices(self) -> List[Device]:
        response = self.__call_get_connected_devices()

        if response.status_code == 401:
            self.credentials = None
            response = self.__call_get_connected_devices()

        response.raise_for_status()

        LOG.debug("getConnDevices response: %s", response.text)

        return to_devices(response.text)

    def __call_get_connected_devices(self) -> requests.Response:
        credentials = self.get_credentials()

        params = {"_n": self.nonce}
        cookies = {"credential": credentials.token}

        return requests.get(f"{self.hostname}/getConnDevices", params=params, cookies=cookies)


@dataclass
class Credentials:
    token: str
    expiration_time: float
