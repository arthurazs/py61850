import unittest
from asn.visible_string import VisibleString
from asn.utils import U8


class TestVisibleStringPack(unittest.TestCase):
    def test_pack_null_string(self):
        self.assertEqual(VisibleString.pack(None), b'\x8A\x00')

    def test_pack_regular_string(self):
        self.assertEqual(VisibleString.pack('arthur'), b'\x8A\x06arthur')

    def test_pack_huge_string(self):
        self.assertEqual(VisibleString.pack('a' * (U8 - 1)), b'\x8A\x81\xFF' + (b'a' * (U8 - 1)))

    # def test_pack_out_of_range(self):
    #     self.assertRaises(ValueError, VisibleString.pack, 'a' * U8)


class TestVisibleStringUnpack(unittest.TestCase):
    def test_unpack_null_string(self):
        self.assertEqual(VisibleString.unpack(b'\x8A\x00'), None)

    def test_unpack_regular_string(self):
        self.assertEqual(VisibleString.unpack(b'\x8A\x06arthur'), 'arthur')

    def test_unpack_huge_string(self):
        self.assertEqual(VisibleString.unpack(b'\x8A\x81\xFF' + (b'a' * (U8 - 1))), 'a' * (U8 - 1))


if __name__ == '__main__':
    unittest.main()
