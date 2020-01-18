import argparse
import sched
import sys

try:
    from arris_tg2492lg import ConnectBox  # The typical way to import arris_tg2492lg
except ImportError:
    # Path hack allows examples to be run without installation.
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0, parentdir)

    from arris_tg2492lg import ConnectBox

s = sched.scheduler()


def main():
    parser = argparse.ArgumentParser(description="Poll device status.")
    parser.add_argument("--host", action="store", dest="host", help="ip-address of the router")
    parser.add_argument("--password", action="store", dest="password", help="password of the router")
    parser.add_argument("--mac", action="store", dest="mac_address", help="mac address of device to poll")

    if len(sys.argv) == 1:
        parser.print_help()
        exit(1)

    args = parser.parse_args()

    connect_box = ConnectBox(args.host, args.password)

    check_device_status(connect_box, args.mac_address)

    s.run()


def check_device_status(connect_box, mac_address):
    devices = connect_box.get_connected_devices()

    matching_devices = [d for d in devices if d.mac == mac_address]

    print("matches:")
    for device in matching_devices:
        print("ip: ", device.ip, ", online: ", device.online)

    s.enter(5, 1, check_device_status, (connect_box, mac_address))


if __name__ == "__main__":
    main()
