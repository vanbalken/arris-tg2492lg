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
    parser = ArgumentParser(description="Get router information.")
    parser.add_argument("--host", action="store", dest="host", help="ip-address of the router")
    parser.add_argument("--password", action="store", dest="password", help="password of the router")

    if len(sys.argv) == 1:
        parser.print_help()
        exit(1)

    args = parser.parse_args()

    async with ClientSession() as session:
        connect_box = ConnectBox(session, args.host, args.password)

        try:
            router_information = await connect_box.async_get_router_information()

            print("MAC address: %s" % router_information.mac_address)
            print("Hardware version: %s" % router_information.hardware_version)
            print("Software version: %s" % router_information.software_version)
            print("Serial number: %s" % router_information.serial_number)

            await connect_box.async_logout()
        except ClientResponseError as exc:
            print("Failed to retrieve router information. Router responded with: %s" % exc.message)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
