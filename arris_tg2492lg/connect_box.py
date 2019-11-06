import base64
import json
import random
import requests

import logging
logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)

from .single_value_cache import SingleValueCache
from .mib_mapper import *

class ConnectBox:
    USERNAME = "admin"
    TOKEN_EXPIRY_TIME = 5 * 60 * 1000

    def __init__(self, host, password):        
        self.host = host
        self.password = password
        self.nonce = random.randrange(10000, 100000)
        self.token = SingleValueCache(ConnectBox.TOKEN_EXPIRY_TIME, self.login)

    def login(self):
        arg_string = ConnectBox.USERNAME + ":" + self.password
        arg = base64.b64encode(arg_string.encode("utf-8")).decode('ascii')

        response = requests.get(self.host + "/login?arg=" + arg + "&_n=" + str(self.nonce))
        response.raise_for_status()

        if not response.text:
            raise Exception("Failed to login")

        token = response.text

        LOG.debug("token: %s", token)

        return token

    def get_connected_devices(self):
        cookies = { 'credential': self.token.get() }
        response = requests.get(self.host + "/getConnDevices?_n=" + str(self.nonce), cookies=cookies)
        response.raise_for_status()

        return to_devices(response.text)
