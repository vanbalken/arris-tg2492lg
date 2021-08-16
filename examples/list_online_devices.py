import asyncio
import sys

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientResponseError
from argparse import ArgumentParser

try:
    from arris_tg2492lg import ConnectBox  # The typical way to import arris_tg2492lg
except ImportError:
    # Path hack allows examples to be run without installation.
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0, parentdir)

    from arris_tg2492lg import ConnectBox


async def main():
    parser = ArgumentParser(description="List MAC addresses of all online devices.")
    parser.add_argument("--host", action="store", dest="host", help="ip-address of the router")
    parser.add_argument("--password", action="store", dest="password", help="password of the router")

    if len(sys.argv) == 1:
        parser.print_help()
        exit(1)

    args = parser.parse_args()

    async with ClientSession() as session:
        connect_box = ConnectBox(session, args.host, args.password)

        try:
            all_devices = await connect_box.async_get_connected_devices()

            devices = []
            mac_addresses = set()

            for device in all_devices:
                if device.online and device.mac not in mac_addresses:
                    devices.append(device)
                    mac_addresses.add(device.mac)

            for device in devices:
                print(device.mac + " " + device.hostname)

            await connect_box.async_logout()
        except ClientResponseError as exc:
            print("Failed to retrieve router information. Router responded with: %s" % exc.message)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
