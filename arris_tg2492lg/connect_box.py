import base64
import logging
import random
import requests
from typing import List

from .device import Device
from .mib_mapper import to_devices
from .single_value_cache import SingleValueCache

LOG = logging.getLogger(__name__)


class ConnectBox:
    USERNAME = "admin"
    TOKEN_EXPIRY_TIME = 5 * 60 * 1000

    def __init__(self, host: str, password: str):
        self.host = host
        self.password = password
        self.nonce = random.randrange(10000, 100000)
        self.token = SingleValueCache(ConnectBox.TOKEN_EXPIRY_TIME, self.login)

    def login(self) -> str:
        arg_string = ConnectBox.USERNAME + ":" + self.password
        arg = base64.b64encode(arg_string.encode("utf-8")).decode("ascii")

        response = requests.get(self.host + "/login?arg=" + arg + "&_n=" + str(self.nonce))
        response.raise_for_status()

        if not response.text:
            raise Exception("Failed to login")

        token = response.text

        LOG.debug("Received token: %s", token)

        return token

    def get_connected_devices(self) -> List[Device]:
        response = self.__call_get_connected_devices()

        if response.status_code == 401:
            self.token.clear()
            response = self.__call_get_connected_devices()

        response.raise_for_status()

        LOG.debug("getConnDevices response: %s", response.text)

        return to_devices(response.text)

    def __call_get_connected_devices(self) -> requests.Response:
        cookies = {"credential": self.token.get()}
        return requests.get(self.host + "/getConnDevices?_n=" + str(self.nonce), cookies=cookies)
