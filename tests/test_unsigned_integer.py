import unittest
from asn.unsigned_integer import UnsignedInt


class TestIntegerPack(unittest.TestCase):
    def test_pack_size_0(self):
        self.assertEqual(UnsignedInt.pack(None), b'\x86\x00')

    def test_pack_size_1_zero(self):
        self.assertEqual(UnsignedInt.pack(0), b'\x86\x01\x00')

    def test_pack_size_1(self):
        self.assertEqual(UnsignedInt.pack(13), b'\x86\x01\x0D')

    def test_pack_size_1_extreme(self):
        self.assertEqual(UnsignedInt.pack(255), b'\x86\x01\xFF')

    def test_pack_size_2(self):
        self.assertEqual(UnsignedInt.pack(256), b'\x86\x02\x01\x00')

    # def test_pack_size_3(self):
    #     self.assertEqual(UnsignedInt.pack(16777215), b'\x86\x03\xFF\xFF\xFF')

    def test_pack_size_4(self):
        self.assertEqual(UnsignedInt.pack(4294967295), b'\x86\x04\xFF\xFF\xFF\xFF')

    def test_pack_negative(self):
        self.assertRaises(ValueError, UnsignedInt.pack, -1)

    def test_pack_out_of_range(self):
        self.assertRaises(ValueError, UnsignedInt.pack, 4294967296)


class TestIntegerUnpack(unittest.TestCase):
    def test_unpack_size_0(self):
        self.assertEqual(UnsignedInt.unpack(b'\x86\x00'), None)

    def test_unpack_size_1(self):
        self.assertEqual(UnsignedInt.unpack(b'\x86\x01\x00'), 0)

    def test_unpack_size_1_extreme(self):
        self.assertEqual(UnsignedInt.unpack(b'\x86\x01\xFF'), 255)

    def test_unpack_size_2(self):
        self.assertEqual(UnsignedInt.unpack(b'\x86\x02\x01\x00'), 256)

    # def test_unpack_size_3(self):
    #     self.assertEqual(UnsignedInt.unpack(b'\x86\x03\xFF\xFF\xFF'), 16777215)

    def test_unpack_size_4(self):
        self.assertEqual(UnsignedInt.unpack(b'\x86\x04\xFF\xFF\xFF\xFF'), 4294967295)

    def test_unpack_out_of_range(self):
        self.assertRaises(ValueError, UnsignedInt.unpack, b'\x86\x05\x01\x00\x00\x00\x00')


if __name__ == '__main__':
    unittest.main()
