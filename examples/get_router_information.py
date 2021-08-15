import asyncio
import aiohttp
import argparse
import sys

try:
    from arris_tg2492lg import ConnectBox  # The typical way to import arris_tg2492lg
except ImportError:
    # Path hack allows examples to be run without installation.
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0, parentdir)

    from arris_tg2492lg import ConnectBox


async def main():
    parser = argparse.ArgumentParser(description="Get router information.")
    parser.add_argument("--host", action="store", dest="host", help="ip-address of the router")
    parser.add_argument("--password", action="store", dest="password", help="password of the router")

    if len(sys.argv) == 1:
        parser.print_help()
        exit(1)

    args = parser.parse_args()

    async with aiohttp.ClientSession() as session:
        connect_box = ConnectBox(session, args.host, args.password)

        try:
            router_information = await connect_box.async_get_router_information()

            print("MAC address: %s" % router_information.mac_address)
            print("Hardware version: %s" % router_information.hardware_version)
            print("Software version: %s" % router_information.software_version)
            print("Serial number: %s" % router_information.serial_number)
        # except Exception as e:
        #     print("Failed to retrieve information of router %s" % args.host)
        #     print(e)
        finally:
            await connect_box.async_logout()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
