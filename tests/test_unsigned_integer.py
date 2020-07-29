import unittest
from asn.unsigned_integer import UnsignedInt
from asn.utils import U8, U16, U32


class TestIntegerPack(unittest.TestCase):
    def test_pack_size_0(self):
        self.assertRaises(ValueError, UnsignedInt.pack, None)

    def test_pack_size_1_zero(self):
        self.assertEqual(UnsignedInt.pack(0), b'\x86\x01\x00')

    def test_pack_size_1_max(self):
        self.assertEqual(UnsignedInt.pack(U8 - 1), b'\x86\x01\xFF')

    def test_pack_size_2_min(self):
        self.assertEqual(UnsignedInt.pack(U8), b'\x86\x02\x01\x00')

    def test_pack_size_2_max(self):
        self.assertEqual(UnsignedInt.pack(U16 - 1), b'\x86\x02\xFF\xFF')

    def test_pack_size_4_min(self):
        self.assertEqual(UnsignedInt.pack(U16), b'\x86\x04\x00\x01\x00\x00')

    def test_pack_size_4_max(self):
        self.assertEqual(UnsignedInt.pack(U32 - 1), b'\x86\x04\xFF\xFF\xFF\xFF')

    def test_pack_negative(self):
        self.assertRaises(ValueError, UnsignedInt.pack, -1)

    def test_pack_out_of_range(self):
        self.assertRaises(ValueError, UnsignedInt.pack, U32)


class TestIntegerUnpack(unittest.TestCase):
    def test_unpack_size_0(self):
        self.assertEqual(UnsignedInt.unpack(b'\x86\x00'), None)

    def test_unpack_size_1_min(self):
        self.assertEqual(UnsignedInt.unpack(b'\x86\x01\x00'), 0)

    def test_unpack_size_1_max(self):
        self.assertEqual(UnsignedInt.unpack(b'\x86\x01\xFF'), U8 - 1)

    def test_unpack_size_2_min(self):
        self.assertEqual(UnsignedInt.unpack(b'\x86\x02\x01\x00'), U8)

    def test_unpack_size_2_max(self):
        self.assertEqual(UnsignedInt.unpack(b'\x86\x02\xFF\xFF'), U16 - 1)

    def test_unpack_size_4_min(self):
        self.assertEqual(UnsignedInt.unpack(b'\x86\x04\x00\x01\x00\x00'), U16)

    def test_unpack_size_4_max(self):
        self.assertEqual(UnsignedInt.unpack(b'\x86\x04\xFF\xFF\xFF\xFF'), U32 - 1)

    def test_unpack_out_of_range(self):
        self.assertRaises(ValueError, UnsignedInt.unpack, b'\x86\x05\x01\x00\x00\x00\x00')


if __name__ == '__main__':
    unittest.main()
