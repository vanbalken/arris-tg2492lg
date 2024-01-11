# Arris TG2492LG Python client

A unofficial Python client for retrieving information from the Arris TG2492LG router. The Arris TG2492LG is one of two routers that Ziggo, a cable operator in the Netherlands, provides to their customers as the Ziggo Connectbox.

The current functionality is limited to retrieving a list of devices that are connected to the router.

> **_WARNING:_** The router prevents the admin user from logging in twice. This can cause problems with accessing the router's configuration pages while using this library. 

## Usage

List all connected devices:

```python
import asyncio
import aiohttp

from arris_tg2492lg import ConnectBox


async def main():
    async with aiohttp.ClientSession() as session:
        connect_box = ConnectBox(session, "http://192.168.178.1", "password")

        devices = await connect_box.async_get_connected_devices()

        print(devices)

        await connect_box.async_logout()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

Please note that the list of connected devices include devices that are offline (e.g. just went out of range of the wifi). The `Device` class contains a property `online` that can be checked.

An example for retrieving a list of the MAC addresses of all online device is included in the `examples` folder:

```bash
python3 list_online_devices.py --host http://192.168.178.1 --password <password>
```

## Development

Setup `arris_tg2492lg` for local development by running:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

```bash
scripts/setup
```

This will create a virtual environment, download the required libraries and configure a git commit hook.
