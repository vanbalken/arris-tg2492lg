import sys

try:
    from arris_tg2492lg import ConnectBox  # The typical way to import arris_tg2492lg
except ImportError:
    # Path hack allows examples to be run without installation.
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0, parentdir)

    from arris_tg2492lg import ConnectBox

def filter_online(device):
    return device.online == "1"

def map_mac_address(device):
    return device.mac

def main():
    '''
    $ python3 list_online_devices.py http://192.168.178.1 <router-password>

    Returns mac addresses of all connected devices that are online.
    '''
    host = sys.argv[1]
    password = sys.argv[2]
    
    connectBox = ConnectBox(host, password)
    devices = connectBox.get_connected_devices()

    # filter out offline devices
    devices = list(filter(filter_online, devices))
    
    # show only mac address
    mac_addresses = list(map(map_mac_address, devices))

    # remove duplicates as some devices are returned with ipv4 and ipv6
    mac_addresses = set(mac_addresses)

    for mac_address in mac_addresses:
        print(mac_address)

if __name__ == "__main__":
    main()
