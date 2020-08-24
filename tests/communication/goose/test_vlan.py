from unittest import TestCase
from py61850.communication.goose.virtual_lan import VirtualLAN
from py61850.utils.numbers import U12

GOOSE_ETHER_TYPE = b'\x88\xb8'
DEFAULT_PRIO = 4
DEFAULT_DESC = 'Video, < 100 ms latency and jitter'
DEFAULT_VID = 0


class TestVLAN(TestCase):
    def setUp(self):
        self.vlan = VirtualLAN(ether_type=GOOSE_ETHER_TYPE, priority=DEFAULT_PRIO, vid=DEFAULT_VID)

    def test_init_min(self):
        vlan = VirtualLAN(ether_type=GOOSE_ETHER_TYPE, priority=0, vid=0)
        self.assertEqual(bytes(vlan), b'\x00\x00' + GOOSE_ETHER_TYPE)

    def test_init_max(self):
        vlan = VirtualLAN(ether_type=GOOSE_ETHER_TYPE, priority=7, vid=U12 - 1)
        self.assertEqual(bytes(vlan), b'\xEF\xFF' + GOOSE_ETHER_TYPE)

    def test_prio_range_error(self):
        with self.assertRaises(ValueError):
            self.vlan.priority = 10

    def test_prio(self):
        self.assertEqual(self.vlan.priority, DEFAULT_PRIO)

    def test_prio_desc(self):
        self.assertEqual(self.vlan.priority_desc, DEFAULT_DESC)

    def test_vid_range_error(self):
        with self.assertRaises(ValueError):
            self.vlan.vid = U12

    def test_vid(self):
        self.assertEqual(self.vlan.vid, DEFAULT_VID)
