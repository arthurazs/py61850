import unittest
from py61850.communication.goose.ethernet import Ethernet
from py61850.utils.numbers import U16, U48, U64


class TestEthernetPackMAC(unittest.TestCase):
    def test_integer_range_error(self):
        self.assertRaises(ValueError, Ethernet.enet_itom, U64)

    def test_integer_type_error(self):
        self.assertRaises(TypeError, Ethernet.enet_itom, '')

    def test_integer_min(self):
        self.assertEqual(Ethernet.enet_itom(0), b'\x00\x00\x00\x00\x00\x00')

    def test_integer_max(self):
        self.assertEqual(Ethernet.enet_itom(U48 - 1), b'\xff\xff\xff\xff\xff\xff')

    def test_ascii_range_error(self):
        self.assertRaises(ValueError, Ethernet.enet_stom, '00:00:00:00:00:00:')

    def test_ascii_malformed(self):
        self.assertRaises(ValueError, Ethernet.enet_stom, '00.00.00.00.00.00')

    def test_ascii_min(self):
        self.assertEqual(Ethernet.enet_stom('000000000000'), b'\x00\x00\x00\x00\x00\x00')

    def test_ascii_max(self):
        self.assertEqual(Ethernet.enet_stom('ffffffffffff'), b'\xff\xff\xff\xff\xff\xff')

    def test_colon_min(self):
        self.assertEqual(Ethernet.enet_stom('00:00:00:00:00:00'), b'\x00\x00\x00\x00\x00\x00')

    def test_colon_max(self):
        self.assertEqual(Ethernet.enet_stom('ff:ff:ff:ff:ff:ff'), b'\xff\xff\xff\xff\xff\xff')

    def test_hyphen_min(self):
        self.assertEqual(Ethernet.enet_stom('00-00-00-00-00-00'), b'\x00\x00\x00\x00\x00\x00')

    def test_hyphen_max(self):
        self.assertEqual(Ethernet.enet_stom('ff-ff-ff-ff-ff-ff'), b'\xff\xff\xff\xff\xff\xff')

    def test_space_min(self):
        self.assertEqual(Ethernet.enet_stom('00 00 00 00 00 00'), b'\x00\x00\x00\x00\x00\x00')

    def test_space_max(self):
        self.assertEqual(Ethernet.enet_stom('ff ff ff ff ff ff'), b'\xff\xff\xff\xff\xff\xff')

    def test_type_error(self):
        self.assertRaises(TypeError, Ethernet.enet_stom, 0)

    def test_pack_bytes(self):
        self.assertEqual(Ethernet.pack_mac_address(b'\x00\x00\x00\x00\x00\x00'), b'\x00\x00\x00\x00\x00\x00')

    def test_pack_string(self):
        self.assertEqual(Ethernet.pack_mac_address('00:00:00:00:00:00'), b'\x00\x00\x00\x00\x00\x00')

    def test_pack_integer(self):
        self.assertEqual(Ethernet.pack_mac_address(0), b'\x00\x00\x00\x00\x00\x00')

    def test_pack_type_error(self):
        self.assertRaises(TypeError, Ethernet.pack_mac_address, 0.0)

    def test_assert_dest_type_error(self):
        self.assertRaises(TypeError, Ethernet.assert_destination, 1)

    def test_assert_dest_value_error_length(self):
        self.assertRaises(ValueError, Ethernet.assert_destination, b'\x01\x0c\xcd\x01')

    def test_assert_dest_value_error_tag(self):
        self.assertRaises(ValueError, Ethernet.assert_destination, b'\x01\x0c\xcd\x02\x00\x00')

    def test_assert_dest_value_error_range(self):
        self.assertRaises(ValueError, Ethernet.assert_destination, b'\x01\x0c\xcd\x01\x02\x00')

    def test_assert_dest(self):
        self.assertTrue(Ethernet.assert_destination(b'\x01\x0c\xcd\x01\x01\xFF'))


class TestEthernetUnpackMAC(unittest.TestCase):
    def test_range_error_below(self):
        self.assertRaises(ValueError, Ethernet.unpack_mac_address, b'\xff\xff\xff\xff\xff')

    def test_range_error_above(self):
        self.assertRaises(ValueError, Ethernet.unpack_mac_address, b'\xff\xff\xff\xff\xff\xff\xff')

    def test_type_error(self):
        self.assertRaises(TypeError, Ethernet.unpack_mac_address, '00-00-00-00-00-00')

    def test_mtos(self):
        self.assertEqual(Ethernet.enet_mtos(b'\x00\x00\x00\x00\x00\x00'), '00-00-00-00-00-00')

    def test_unpack_splitter(self):
        self.assertEqual(Ethernet.unpack_mac_address(b'\xff\xff\xff\xff\xff\xff', ':'), 'FF:FF:FF:FF:FF:FF')


class TestEthernetPackEtherType(unittest.TestCase):
    def test_itoe_type_error(self):
        self.assertRaises(TypeError, Ethernet.enet_itoe, '0000')

    def test_itoe_range_error(self):
        self.assertRaises(ValueError, Ethernet.enet_itoe, U16)

    def test_itoe_min(self):
        self.assertEqual(Ethernet.enet_itoe(0), b'\x00\x00')

    def test_itoe_max(self):
        self.assertEqual(Ethernet.enet_itoe(U16 - 1), b'\xff\xff')

    def test_stoe_type_error(self):
        self.assertRaises(TypeError, Ethernet.enet_stoe, 0)

    def test_stoe_length_error_below(self):
        self.assertRaises(ValueError, Ethernet.enet_stoe, '123')

    def test_stoe_length_error_above(self):
        self.assertRaises(ValueError, Ethernet.enet_stoe, '12345')

    def test_stoe_min(self):
        self.assertEqual(Ethernet.enet_stoe('0000'), b'\x00\x00')

    def test_stoe_max(self):
        self.assertEqual(Ethernet.enet_stoe('ffff'), b'\xff\xff')

    def test_pack_type_error(self):
        self.assertRaises(TypeError, Ethernet.pack_ether_type, 0.0)

    def test_pack_bytes(self):
        self.assertEqual(Ethernet.pack_ether_type(b'\x00\x00'), b'\x00\x00')

    def test_pack_integer(self):
        self.assertEqual(Ethernet.pack_ether_type(0), b'\x00\x00')

    def test_pack_string(self):
        self.assertEqual(Ethernet.pack_ether_type('0000'), b'\x00\x00')


class TestEthernetUnpackEtherType(unittest.TestCase):
    def test_etos_type_error(self):
        self.assertRaises(TypeError, Ethernet.enet_etos, '0000')

    def test_etos_length_error_below(self):
        self.assertRaises(ValueError, Ethernet.enet_etos, b'\x00')

    def test_etos_length_error_above(self):
        self.assertRaises(ValueError, Ethernet.enet_etos, b'\x00\x00\x00')

    def test_etos(self):
        self.assertEqual(Ethernet.enet_etos(b'\x12\xab'), '12AB')


if __name__ == '__main__':
    unittest.main()
