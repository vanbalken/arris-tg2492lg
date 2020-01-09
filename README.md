# Arris TG2492LG Python client

A unofficial Python client for retrieving information from the Arris TG2492LG router. The Arris TG2492LG is one of two routers that Ziggo, a cable operator in the Netherlands, provides to their customers as Ziggo Connectbox.

The current functionality is limited to retrieving a list of devices that are connected to the router.

## Usage

List all connected devices:

```python
from arris_tg2492lg import ConnectBox

connectBox = ConnectBox("http://192.168.178.1", "password")
devices = connectBox.get_connected_devices()

print(devices)

```

Please note that the list of connected devices include devices that are offline (e.g. just went out of range of the wifi). The `Device` class contains a property `online` that can be checked.

An example for retrieving a list of the MAC addresses of all online device is included in the `examples` folder:

```bash
python3 list_online_devices.py --host http://192.168.178.1 --password <password>
```
