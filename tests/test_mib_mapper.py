import unittest
import ipaddress

from arris_tg2492lg import mib_mapper

class TestMibMapper(unittest.TestCase):
    def test_to_devices(self):
        get_conn_devices_json = """
            {
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.3.200.1.4.192.168.178.2":"My Device",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.4.200.1.4.192.168.178.2":"$1234567890AB",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.6.200.1.4.192.168.178.2":"5",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.7.200.1.4.192.168.178.2":"1",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.9.200.1.4.192.168.178.2":"$07e30b0310330400",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.13.200.1.4.192.168.178.2":"1",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.14.200.1.4.192.168.178.2":"1",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.15.200.1.4.192.168.178.2":"",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.20.200.1.4.192.168.178.2":"unknown device",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.3.200.1.4.192.168.178.3":"My Device 2",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.4.200.1.4.192.168.178.3":"$BA0987654321",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.6.200.1.4.192.168.178.3":"21",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.7.200.1.4.192.168.178.3":"5",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.9.200.1.4.192.168.178.3":"$0000000000000000",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.13.200.1.4.192.168.178.3":"1",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.14.200.1.4.192.168.178.3":"1",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.15.200.1.4.192.168.178.3":"",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.20.200.1.4.192.168.178.3":"unknown device",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.3.200.2.16.32.1.28.18.8.214.187.0.176.246.133.90.13.205.85.40":"My Device 3",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.4.200.2.16.32.1.28.18.8.214.187.0.176.246.133.90.13.205.85.40":"$AAAAAAAAAAAA",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.6.200.2.16.32.1.28.18.8.214.187.0.176.246.133.90.13.205.85.40":"21",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.7.200.2.16.32.1.28.18.8.214.187.0.176.246.133.90.13.205.85.40":"5",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.9.200.2.16.32.1.28.18.8.214.187.0.176.246.133.90.13.205.85.40":"$0000000000000000",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.13.200.2.16.32.1.28.18.8.214.187.0.176.246.133.90.13.205.85.40":"1",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.14.200.2.16.32.1.28.18.8.214.187.0.176.246.133.90.13.205.85.40":"1",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.15.200.2.16.32.1.28.18.8.214.187.0.176.246.133.90.13.205.85.40":"",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.20.200.2.16.32.1.28.18.8.214.187.0.176.246.133.90.13.205.85.40":"device 3",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.3.200.2.16.32.1.28.18.8.214.187.0.176.246.133.90.13.205.85.41":"My Device",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.4.200.2.16.32.1.28.18.8.214.187.0.176.246.133.90.13.205.85.41":"$1234567890AB",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.6.200.2.16.32.1.28.18.8.214.187.0.176.246.133.90.13.205.85.41":"5",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.7.200.2.16.32.1.28.18.8.214.187.0.176.246.133.90.13.205.85.41":"1",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.9.200.2.16.32.1.28.18.8.214.187.0.176.246.133.90.13.205.85.41":"$07e30b0310330400",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.13.200.2.16.32.1.28.18.8.214.187.0.176.246.133.90.13.205.85.41":"1",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.14.200.2.16.32.1.28.18.8.214.187.0.176.246.133.90.13.205.85.41":"1",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.15.200.2.16.32.1.28.18.8.214.187.0.176.246.133.90.13.205.85.41":"",
                "1.3.6.1.4.1.4115.1.20.1.1.2.4.2.1.20.200.2.16.32.1.28.18.8.214.187.0.176.246.133.90.13.205.85.41":"unknown device",
                "1": "Finish"
            }
        """

        devices = mib_mapper.to_devices(get_conn_devices_json)

        self.assertEqual(len(devices), 4)

        device = devices[0]

        self.assertEqual(device.ip, ipaddress.ip_address("192.168.178.2"))
        self.assertEqual(device.hostname, "My Device")
        self.assertEqual(device.mac, "12:34:56:78:90:AB")
        self.assertEqual(device.adapter_type, "wireless1")
        self.assertEqual(device.type, "1")
        self.assertEqual(device.lease_end, "2019-11-03 16:51:04:00")
        self.assertEqual(device.row_status, "1")
        self.assertEqual(device.online, True)
        self.assertEqual(device.comment, "")
        self.assertEqual(device.device_name, "unknown device")

        device2 = devices[1]

        self.assertEqual(device2.ip, ipaddress.ip_address("192.168.178.3"))
        self.assertEqual(device2.hostname, "My Device 2")
        self.assertEqual(device2.mac, "BA:09:87:65:43:21")
        self.assertEqual(device2.adapter_type, "ethernet2")
        self.assertEqual(device2.type, "5")
        self.assertEqual(device2.lease_end, "0000-00-00 00:00:00:00")
        self.assertEqual(device2.row_status, "1")
        self.assertEqual(device2.online, True)
        self.assertEqual(device2.comment, "")
        self.assertEqual(device2.device_name, "unknown device")

        device3 = devices[2]

        self.assertEqual(device3.ip, ipaddress.ip_address("2001:1c12:8d6:bb00:b0f6:855a:dcd:5528"))
        self.assertEqual(device3.hostname, "My Device 3")
        self.assertEqual(device3.mac, "AA:AA:AA:AA:AA:AA")
        self.assertEqual(device3.adapter_type, "ethernet2")
        self.assertEqual(device3.type, "5")
        self.assertEqual(device3.lease_end, "0000-00-00 00:00:00:00")
        self.assertEqual(device3.row_status, "1")
        self.assertEqual(device3.online, True)
        self.assertEqual(device3.comment, "")
        self.assertEqual(device3.device_name, "device 3")

        device4 = devices[3]
        
        self.assertEqual(device4.ip, ipaddress.ip_address("2001:1c12:8d6:bb00:b0f6:855a:dcd:5529"))
        self.assertEqual(device4.hostname, "My Device")
        self.assertEqual(device4.mac, "12:34:56:78:90:AB")
        self.assertEqual(device4.adapter_type, "wireless1")
        self.assertEqual(device4.type, "1")
        self.assertEqual(device4.lease_end, "2019-11-03 16:51:04:00")
        self.assertEqual(device4.row_status, "1")
        self.assertEqual(device4.online, True)
        self.assertEqual(device4.comment, "")
        self.assertEqual(device4.device_name, "unknown device")
