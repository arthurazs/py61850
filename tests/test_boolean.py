import unittest
from iec.boolean import Boolean


class TestBooleanPack(unittest.TestCase):
    def test_pack_true(self):
        self.assertEqual(Boolean.pack(True), b'\x83\x01\x0F')

    def test_pack_false(self):
        self.assertEqual(Boolean.pack(False), b'\x83\x01\x00')

    def test_pack_none(self):
        self.assertRaises(ValueError, Boolean.pack, None)


class TestBooleanUnpack(unittest.TestCase):
    def test_unpack_partial_true(self):
        self.assertEqual(Boolean.unpack(b'\x83\x01\x0F'), True)

    def test_unpack_full_true(self):
        self.assertEqual(Boolean.unpack(b'\x83\x01\xFF'), True)

    def test_unpack_false(self):
        self.assertEqual(Boolean.unpack(b'\x83\x01\x00'), False)

    def test_unpack_none(self):
        self.assertEqual(Boolean.unpack(b'\x83\x00'), None)

    def test_unpack_different_size(self):
        self.assertRaises(ValueError, Boolean.unpack, b'\x83\x02\x00\x00')


if __name__ == '__main__':
    unittest.main()
