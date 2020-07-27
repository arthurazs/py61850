import unittest
from asn.signed_integer import SignedInt


class TestIntegerPack(unittest.TestCase):
    def test_pack_size_0(self):
        self.assertEqual(SignedInt.pack(None), b'\x85\x00')

    def test_pack_size_1_zero(self):
        self.assertEqual(SignedInt.pack(0), b'\x85\x01\x00')

    def test_pack_size_1_negative(self):
        self.assertEqual(SignedInt.pack(-13), b'\x85\x01\xF3')

    def test_pack_size_1_positive(self):
        self.assertEqual(SignedInt.pack(13), b'\x85\x01\x0D')

    def test_pack_size_1_extreme_negative(self):
        self.assertEqual(SignedInt.pack(-128), b'\x85\x01\x80')

    def test_pack_size_1_extreme_positive(self):
        self.assertEqual(SignedInt.pack(127), b'\x85\x01\x7F')

    def test_pack_size_2(self):
        self.assertEqual(SignedInt.pack(256), b'\x85\x02\x01\x00')

    def test_pack_size_4(self):
        self.assertEqual(SignedInt.pack(-16777210), b'\x85\x04\xFF\x00\x00\x06')

    def test_pack_size_8(self):
        self.assertEqual(SignedInt.pack(4294967295), b'\x85\x08\x00\x00\x00\x00\xFF\xFF\xFF\xFF')

    def test_pack_out_of_range(self):
        self.assertRaises(ValueError, SignedInt.pack, 9223372036854775808)


class TestIntegerUnpack(unittest.TestCase):
    def test_pack_size_0(self):
        self.assertEqual(SignedInt.unpack(b'\x85\x00'), None)

    def test_pack_size_1_zero(self):
        self.assertEqual(SignedInt.unpack(b'\x85\x01\x00'), 0)

    def test_pack_size_1_negative(self):
        self.assertEqual(SignedInt.unpack(b'\x85\x01\xF3'), -13)

    def test_pack_size_1_positive(self):
        self.assertEqual(SignedInt.unpack(b'\x85\x01\x0D'), 13)

    def test_pack_size_1_extreme_negative(self):
        self.assertEqual(SignedInt.unpack(b'\x85\x01\x80'), -128)

    def test_pack_size_1_extreme_positive(self):
        self.assertEqual(SignedInt.unpack(b'\x85\x01\x7F'), 127)

    def test_pack_size_2(self):
        self.assertEqual(SignedInt.unpack(b'\x85\x02\x01\x00'), 256)

    def test_pack_size_4(self):
        self.assertEqual(SignedInt.unpack(b'\x85\x04\xFF\x00\x00\x06'), -16777210)

    def test_pack_size_8(self):
        self.assertEqual(SignedInt.unpack(b'\x85\x08\x00\x00\x00\x00\xFF\xFF\xFF\xFF'), 4294967295)

    def test_pack_out_of_range(self):
        self.assertRaises(ValueError, SignedInt.unpack, b'\x85\x09\x7f\xff\xff\xff\xff\xff\xff\xff\xff')


if __name__ == '__main__':
    unittest.main()
