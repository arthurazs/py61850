import unittest
from asn.generic_asn import GenericASN


class TestGenericASN(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        GenericASN.TAG = b'\x86'

    def test_unpack_wrong_tag(self):
        self.assertRaises(TypeError, GenericASN.get_asn, b'\x87\x00')

    def test_unpack_missing_size(self):
        self.assertRaises(ValueError, GenericASN.get_asn, b'\x86')

    def test_unpack_bigger_size(self):
        self.assertRaises(ValueError, GenericASN.get_asn, b'\x86\x03\xFF\xFF\xFF\xFF')

    def test_unpack_smaller_size(self):
        self.assertRaises(ValueError, GenericASN.get_asn, b'\x86\x03\xFF\xFF')


if __name__ == '__main__':
    unittest.main()
