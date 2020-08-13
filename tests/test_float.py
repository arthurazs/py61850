import unittest
from iec.floating_point import FloatingPoint
from math import isnan
from iec.utils import PI32, PI64, ONE_THIRD32, ONE_THIRD64


class TestFloatingPointSinglePrecisionPack(unittest.TestCase):
    def test_pack_size_0(self):
        self.assertRaises(ValueError, FloatingPoint.pack, None)

    def test_pack_zero_int(self):
        self.assertEqual(FloatingPoint.pack(0), b'\x87\x05\x08\x00\x00\x00\x00')

    def test_pack_positive_zero(self):
        self.assertEqual(FloatingPoint.pack(0.0), b'\x87\x05\x08\x00\x00\x00\x00')

    def test_pack_negative_zero(self):
        self.assertEqual(FloatingPoint.pack(-0.0), b'\x87\x05\x08\x80\x00\x00\x00')

    def test_pack_positive_two(self):
        self.assertEqual(FloatingPoint.pack(2), b'\x87\x05\x08\x40\x00\x00\x00')

    def test_pack_negative_two(self):
        self.assertEqual(FloatingPoint.pack(-2), b'\x87\x05\x08\xc0\x00\x00\x00')

    def test_pack_smallest_positive(self):
        self.assertEqual(FloatingPoint.pack(1e-45), b'\x87\x05\x08\x00\x00\x00\x01')

    def test_pack_smallest_negative(self):
        self.assertEqual(FloatingPoint.pack(-1e-45), b'\x87\x05\x08\x80\x00\x00\x01')

    def test_pack_largest_positive(self):
        self.assertEqual(FloatingPoint.pack(3.4028234e38), b'\x87\x05\x08\x7f\x7f\xff\xff')

    def test_pack_largest_negative(self):
        self.assertEqual(FloatingPoint.pack(-3.4028234e38), b'\x87\x05\x08\xff\x7f\xff\xff')

    def test_pack_inf_positive(self):
        self.assertEqual(FloatingPoint.pack(float('inf')), b'\x87\x05\x08\x7f\x80\x00\x00')

    def test_pack_inf_negative(self):
        self.assertEqual(FloatingPoint.pack(float('-inf')), b'\x87\x05\x08\xff\x80\x00\x00')

    def test_pack_pi_positive(self):
        self.assertEqual(FloatingPoint.pack(PI32), b'\x87\x05\x08\x40\x49\x0f\xdb')

    def test_pack_pi_negative(self):
        self.assertEqual(FloatingPoint.pack(-PI32), b'\x87\x05\x08\xc0\x49\x0f\xdb')

    def test_pack_one_third_positive(self):
        self.assertEqual(FloatingPoint.pack(ONE_THIRD32), b'\x87\x05\x08\x3e\xaa\xaa\xab')

    def test_pack_one_third_negative(self):
        self.assertEqual(FloatingPoint.pack(-ONE_THIRD32), b'\x87\x05\x08\xbe\xaa\xaa\xab')

    def test_pack_nan_positive(self):
        self.assertEqual(FloatingPoint.pack(float('nan')), b'\x87\x05\x08\x7f\xc0\x00\x00')

    def test_pack_nan_negative(self):
        self.assertEqual(FloatingPoint.pack(float('-nan')), b'\x87\x05\x08\xff\xc0\x00\x00')


class TestFloatingPointSinglePrecisionUnpack(unittest.TestCase):
    def test_unpack_size_0(self):
        self.assertEqual(FloatingPoint.unpack(b'\x87\x00'), None)

    def test_unpack_size_1(self):
        self.assertEqual(FloatingPoint.unpack(b'\x87\x01\x08'), None)

    def test_unpack_positive_zero(self):
        self.assertEqual(FloatingPoint.unpack(b'\x87\x05\x08\x00\x00\x00\x00'), 0)

    def test_unpack_negative_zero(self):
        self.assertEqual(FloatingPoint.unpack(b'\x87\x05\x08\x80\x00\x00\x00'), -0)

    def test_unpack_positive_two(self):
        self.assertEqual(FloatingPoint.unpack(b'\x87\x05\x08\x40\x00\x00\x00'), 2)

    def test_unpack_negative_two(self):
        self.assertEqual(FloatingPoint.unpack(b'\x87\x05\x08\xc0\x00\x00\x00'), -2)

    def test_unpack_smallest_positive(self):
        self.assertEqual(FloatingPoint.unpack(b'\x87\x05\x08\x00\x00\x00\x01'), 1.401298464324817e-45)

    def test_unpack_smallest_negative(self):
        self.assertEqual(FloatingPoint.unpack(b'\x87\x05\x08\x80\x00\x00\x01'), -1.401298464324817e-45)

    def test_unpack_largest_positive(self):
        self.assertEqual(FloatingPoint.unpack(b'\x87\x05\x08\x7f\x7f\xff\xff'), 3.4028234663852886e+38)

    def test_unpack_largest_negative(self):
        self.assertEqual(FloatingPoint.unpack(b'\x87\x05\x08\xff\x7f\xff\xff'), -3.4028234663852886e+38)

    def test_unpack_inf_positive(self):
        self.assertEqual(FloatingPoint.unpack(b'\x87\x05\x08\x7f\x80\x00\x00'), float('inf'))

    def test_unpack_inf_negative(self):
        self.assertEqual(FloatingPoint.unpack(b'\x87\x05\x08\xff\x80\x00\x00'), float('-inf'))

    def test_unpack_pi_positive(self):
        self.assertEqual(FloatingPoint.unpack(b'\x87\x05\x08\x40\x49\x0f\xdb'), PI32)

    def test_unpack_pi_negative(self):
        self.assertEqual(FloatingPoint.unpack(b'\x87\x05\x08\xc0\x49\x0f\xdb'), -PI32)

    def test_unpack_one_third_positive(self):
        self.assertEqual(FloatingPoint.unpack(b'\x87\x05\x08\x3e\xaa\xaa\xab'), ONE_THIRD32)

    def test_unpack_one_third_negative(self):
        self.assertEqual(FloatingPoint.unpack(b'\x87\x05\x08\xbe\xaa\xaa\xab'), -ONE_THIRD32)

    def test_unpack_nan_positive(self):
        self.assertTrue(isnan(FloatingPoint.unpack(b'\x87\x05\x08\x7f\xc0\x00\x00')))

    def test_unpack_nan_negative(self):
        self.assertTrue(isnan(FloatingPoint.unpack(b'\x87\x05\x08\xff\xc0\x00\x00')))

    def test_unpack_wrong_size(self):
        self.assertRaises(ValueError, FloatingPoint.unpack, b'\x87\x04\x08\x00\x00\x00')

    def test_unpack_wrong_type(self):
        self.assertRaises(TypeError, FloatingPoint.unpack, b'\x87\x05\x09\x00\x00\x00\x00')


class TestFloatingPointDoublePrecisionPack(unittest.TestCase):
    def test_pack_size_0(self):
        self.assertRaises(ValueError, FloatingPoint.pack, None, double_precision=True)

    def test_pack_zero_int(self):
        self.assertEqual(
            FloatingPoint.pack(0, double_precision=True),
            b'\x87\x09\x11\x00\x00\x00\x00\x00\x00\x00\x00')

    def test_pack_positive_zero(self):
        self.assertEqual(
            FloatingPoint.pack(0.0, double_precision=True),
            b'\x87\x09\x11\x00\x00\x00\x00\x00\x00\x00\x00')

    def test_pack_negative_zero(self):
        self.assertEqual(
            FloatingPoint.pack(-0.0, double_precision=True),
            b'\x87\x09\x11\x80\x00\x00\x00\x00\x00\x00\x00')

    def test_pack_positive_two(self):
        self.assertEqual(
            FloatingPoint.pack(2, double_precision=True),
            b'\x87\x09\x11\x40\x00\x00\x00\x00\x00\x00\x00')

    def test_pack_negative_two(self):
        self.assertEqual(
            FloatingPoint.pack(-2, double_precision=True),
            b'\x87\x09\x11\xc0\x00\x00\x00\x00\x00\x00\x00')

    def test_pack_smallest_positive(self):
        self.assertEqual(
            FloatingPoint.pack(5e-324, double_precision=True),
            b'\x87\x09\x11\x00\x00\x00\x00\x00\x00\x00\x01')

    def test_pack_smallest_negative(self):
        self.assertEqual(
            FloatingPoint.pack(-5e-324, double_precision=True),
            b'\x87\x09\x11\x80\x00\x00\x00\x00\x00\x00\x01')

    def test_pack_largest_positive(self):
        self.assertEqual(
            FloatingPoint.pack(1.7976931348623157e+308, double_precision=True),
            b'\x87\x09\x11\x7f\xef\xff\xff\xff\xff\xff\xff')

    def test_pack_largest_negative(self):
        self.assertEqual(
            FloatingPoint.pack(-1.7976931348623157e+308, double_precision=True),
            b'\x87\x09\x11\xff\xef\xff\xff\xff\xff\xff\xff')

    def test_pack_inf_positive(self):
        self.assertEqual(
            FloatingPoint.pack(float('inf'), double_precision=True),
            b'\x87\x09\x11\x7f\xf0\x00\x00\x00\x00\x00\x00')

    def test_pack_inf_negative(self):
        self.assertEqual(
            FloatingPoint.pack(float('-inf'), double_precision=True),
            b'\x87\x09\x11\xff\xf0\x00\x00\x00\x00\x00\x00')

    def test_pack_pi_positive(self):
        self.assertEqual(
            FloatingPoint.pack(PI64, double_precision=True),
            b'\x87\x09\x11\x40\x09\x21\xfb\x54\x44\x2d\x18')

    def test_pack_pi_negative(self):
        self.assertEqual(
            FloatingPoint.pack(-PI64, double_precision=True),
            b'\x87\x09\x11\xc0\x09\x21\xfb\x54\x44\x2d\x18')

    def test_pack_one_third_positive(self):
        self.assertEqual(
            FloatingPoint.pack(ONE_THIRD64, double_precision=True),
            b'\x87\x09\x11\x3f\xd5\x55\x55\x55\x55\x55\x55')

    def test_pack_one_third_negative(self):
        self.assertEqual(
            FloatingPoint.pack(-ONE_THIRD64, double_precision=True),
            b'\x87\x09\x11\xbf\xd5\x55\x55\x55\x55\x55\x55')

    def test_pack_nan_positive(self):
        self.assertEqual(
            FloatingPoint.pack(float('nan'), double_precision=True),
            b'\x87\x09\x11\x7f\xf8\x00\x00\x00\x00\x00\x00')

    def test_pack_nan_negative(self):
        self.assertEqual(
            FloatingPoint.pack(float('-nan'), double_precision=True),
            b'\x87\x09\x11\xff\xf8\x00\x00\x00\x00\x00\x00')


class TestFloatingPointDoublePrecisionUnpack(unittest.TestCase):
    def test_unpack_size_0(self):
        self.assertEqual(
            FloatingPoint.unpack(b'\x87\x00'),
            None)

    def test_unpack_size_1(self):
        self.assertEqual(
            FloatingPoint.unpack(b'\x87\x01\x11'),
            None)

    def test_unpack_positive_zero(self):
        self.assertEqual(
            FloatingPoint.unpack(b'\x87\x09\x11\x00\x00\x00\x00\x00\x00\x00\x00'),
            0)

    def test_unpack_negative_zero(self):
        self.assertEqual(
            FloatingPoint.unpack(b'\x87\x09\x11\x80\x00\x00\x00\x00\x00\x00\x00'),
            -0)

    def test_unpack_positive_two(self):
        self.assertEqual(FloatingPoint.unpack(
            b'\x87\x09\x11\x40\x00\x00\x00\x00\x00\x00\x00'),
            2)

    def test_unpack_negative_two(self):
        self.assertEqual(
            FloatingPoint.unpack(b'\x87\x09\x11\xc0\x00\x00\x00\x00\x00\x00\x00'),
            -2)

    def test_unpack_smallest_positive(self):
        self.assertEqual(
            FloatingPoint.unpack(b'\x87\x09\x11\x00\x00\x00\x00\x00\x00\x00\x01'),
            5e-324)

    def test_unpack_smallest_negative(self):
        self.assertEqual(
            FloatingPoint.unpack(b'\x87\x09\x11\x80\x00\x00\x00\x00\x00\x00\x01'),
            -5e-324)

    def test_unpack_largest_positive(self):
        self.assertEqual(
            FloatingPoint.unpack(b'\x87\x09\x11\x7f\xef\xff\xff\xff\xff\xff\xff'),
            1.7976931348623157e+308)

    def test_unpack_largest_negative(self):
        self.assertEqual(
            FloatingPoint.unpack(b'\x87\x09\x11\xff\xef\xff\xff\xff\xff\xff\xff'),
            -1.7976931348623157e+308)

    def test_unpack_inf_positive(self):
        self.assertEqual(
            FloatingPoint.unpack(b'\x87\x09\x11\x7f\xf0\x00\x00\x00\x00\x00\x00'),
            float('inf'))

    def test_unpack_inf_negative(self):
        self.assertEqual(
            FloatingPoint.unpack(b'\x87\x09\x11\xff\xf0\x00\x00\x00\x00\x00\x00'),
            float('-inf'))

    def test_unpack_pi_positive(self):
        self.assertEqual(
            FloatingPoint.unpack(b'\x87\x09\x11\x40\x09\x21\xfb\x54\x44\x2d\x18'),
            PI64)

    def test_unpack_pi_negative(self):
        self.assertEqual(
            FloatingPoint.unpack(b'\x87\x09\x11\xc0\x09\x21\xfb\x54\x44\x2d\x18'),
            -PI64)

    def test_unpack_one_third_positive(self):
        self.assertEqual(
            FloatingPoint.unpack(b'\x87\x09\x11\x3f\xd5\x55\x55\x55\x55\x55\x55'),
            ONE_THIRD64)

    def test_unpack_one_third_negative(self):
        self.assertEqual(
            FloatingPoint.unpack(b'\x87\x09\x11\xbf\xd5\x55\x55\x55\x55\x55\x55'),
            -ONE_THIRD64)

    def test_unpack_nan_positive(self):
        self.assertTrue(isnan(
            FloatingPoint.unpack(b'\x87\x09\x11\x7f\xf8\x00\x00\x00\x00\x00\x00')))

    def test_unpack_nan_negative(self):
        self.assertTrue(isnan(
            FloatingPoint.unpack(b'\x87\x09\x11\xff\xf8\x00\x00\x00\x00\x00\x00')))

    def test_unpack_wrong_size(self):
        self.assertRaises(ValueError, FloatingPoint.unpack, b'\x87\x08\x11\x00\x00\x00\x00\x00\x00\x00')

    def test_unpack_wrong_type(self):
        self.assertRaises(TypeError, FloatingPoint.unpack, b'\x87\x09\x10\x00\x00\x00\x00\x00\x00\x00\x00')


if __name__ == '__main__':
    unittest.main()
