import unittest
from iec.signed_integer import SignedInt
from iec.utils import N8, P8, N16, P16, N32, P32, N64, P64


class TestIntegerPack(unittest.TestCase):
    def test_pack_size_0(self):
        self.assertRaises(ValueError, SignedInt.pack, None)

    def test_pack_size_1_zero(self):
        self.assertEqual(SignedInt.pack(0), b'\x85\x01\x00')

    def test_pack_size_1_min(self):
        self.assertEqual(SignedInt.pack(N8), b'\x85\x01\x80')

    def test_pack_size_1_max(self):
        self.assertEqual(SignedInt.pack(P8), b'\x85\x01\x7F')

    def test_pack_size_2_min(self):
        self.assertEqual(SignedInt.pack(N16), b'\x85\x02\x80\x00')

    def test_pack_size_2_max(self):
        self.assertEqual(SignedInt.pack(P16), b'\x85\x02\x7F\xFF')

    def test_pack_size_4_min(self):
        self.assertEqual(SignedInt.pack(N32), b'\x85\x04\x80\x00\x00\x00')

    def test_pack_size_4_max(self):
        self.assertEqual(SignedInt.pack(P32), b'\x85\x04\x7F\xFF\xFF\xFF')

    def test_pack_size_8_min(self):
        self.assertEqual(SignedInt.pack(N64), b'\x85\x08\x80\x00\x00\x00\x00\x00\x00\x00')

    def test_pack_size_8_max(self):
        self.assertEqual(SignedInt.pack(P64), b'\x85\x08\x7F\xFF\xFF\xFF\xFF\xFF\xFF\xFF')

    def test_pack_out_of_range(self):
        self.assertRaises(ValueError, SignedInt.pack, P64 + 1)


class TestIntegerUnpack(unittest.TestCase):
    def test_pack_size_0(self):
        self.assertEqual(SignedInt.unpack(b'\x85\x00'), None)

    def test_pack_size_1_zero(self):
        self.assertEqual(SignedInt.unpack(b'\x85\x01\x00'), 0)

    def test_pack_size_1_min(self):
        self.assertEqual(SignedInt.unpack(b'\x85\x01\x80'), N8)

    def test_pack_size_1_max(self):
        self.assertEqual(SignedInt.unpack(b'\x85\x01\x7F'), P8)

    def test_pack_size_2_min(self):
        self.assertEqual(SignedInt.unpack(b'\x85\x02\x80\x00'), N16)

    def test_pack_size_2_max(self):
        self.assertEqual(SignedInt.unpack(b'\x85\x02\x7F\xFF'), P16)

    def test_pack_size_4_min(self):
        self.assertEqual(SignedInt.unpack(b'\x85\x04\x80\x00\x00\x00'), N32)

    def test_pack_size_4_max(self):
        self.assertEqual(SignedInt.unpack(b'\x85\x04\x7F\xFF\xFF\xFF'), P32)

    def test_pack_size_8_min(self):
        self.assertEqual(SignedInt.unpack(b'\x85\x08\x80\x00\x00\x00\x00\x00\x00\x00'), N64)

    def test_pack_size_8_max(self):
        self.assertEqual(SignedInt.unpack(b'\x85\x08\x7f\xff\xff\xff\xff\xff\xff\xff'), P64)

    def test_pack_out_of_range(self):
        self.assertRaises(ValueError, SignedInt.unpack, b'\x85\x09\x7f\xff\xff\xff\xff\xff\xff\xff\xff')


if __name__ == '__main__':
    unittest.main()
