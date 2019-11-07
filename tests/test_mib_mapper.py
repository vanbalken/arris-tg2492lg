import unittest

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
                "1": "Finish"
            }
        """

        devices = mib_mapper.to_devices(get_conn_devices_json)

        self.assertEqual(len(devices), 2)

        device = devices[0]

        self.assertEqual(device.ip, "192.168.178.2")
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

        self.assertEqual(device2.ip, "192.168.178.3")
        self.assertEqual(device2.hostname, "My Device 2")
        self.assertEqual(device2.mac, "BA:09:87:65:43:21")
        self.assertEqual(device2.adapter_type, "ethernet2")
        self.assertEqual(device2.type, "5")
        self.assertEqual(device2.lease_end, "0000-00-00 00:00:00:00")
        self.assertEqual(device2.row_status, "1")
        self.assertEqual(device2.online, True)
        self.assertEqual(device2.comment, "")
        self.assertEqual(device2.device_name, "unknown device")
