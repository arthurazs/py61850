from pytest import fixture, raises
from pytest import mark

from py61850.types.floating_point import SinglePrecision, DoublePrecision
from math import isnan

test_data_single = {
    id: [
        'zero_negative', 'zero_positive',
        'min_negative', 'min_positive',
        'max_negative', 'max_positive',
        'pi_negative', 'pi_positive',
        'one_third_negative', 'one_third_positive',
        'inf_negative', 'inf_positive',
    ],
    float: [
        -0.0, 0.0,                                          # Zero
        -1.401298464324817e-45, 1.401298464324817e-45,      # Smallest
        -3.4028234663852886e+38, 3.4028234663852886e+38,    # Largest
        -3.1415927410125732, 3.1415927410125732,            # PI
        -0.3333333432674408, 0.3333333432674408,            # 1/3
        float('-inf'), float('inf'),                        # Infinity
    ],
    bytes: [
        b'\x08\x80\x00\x00\x00', b'\x08\x00\x00\x00\x00',   # Zero
        b'\x08\x80\x00\x00\x01', b'\x08\x00\x00\x00\x01',   # Smallest
        b'\x08\xFF\x7F\xFF\xFF', b'\x08\x7F\x7F\xFF\xFF',   # Largest
        b'\x08\xC0\x49\x0F\xDB', b'\x08\x40\x49\x0F\xDB',   # PI
        b'\x08\xBE\xAA\xAA\xAB', b'\x08\x3E\xAA\xAA\xAB',   # 1/3
        b'\x08\xFF\x80\x00\x00', b'\x08\x7F\x80\x00\x00',   # Infinity
    ],
}

test_data_double = {
    id: [
        'zero_negative', 'zero_positive',
        'min_negative', 'min_positive',
        'max_negative', 'max_positive',
        'pi_negative', 'pi_positive',
        'one_third_negative', 'one_third_positive',
        'inf_negative', 'inf_positive',
    ],
    float: [
        -0.0, 0.0,                                          # Zero
        -5e-324, 5e-324,                                    # Smallest
        -1.7976931348623157e+308, 1.7976931348623157e+308,  # Largest
        -3.141592653589793, 3.141592653589793,              # PI
        -0.3333333333333333, 0.3333333333333333,            # 1/3
        float('-inf'), float('inf'),                        # Infinity
    ],
    bytes: [
        b'\x11\x80\x00\x00\x00\x00\x00\x00\x00', b'\x11\x00\x00\x00\x00\x00\x00\x00\x00',   # Zero
        b'\x11\x80\x00\x00\x00\x00\x00\x00\x01', b'\x11\x00\x00\x00\x00\x00\x00\x00\x01',   # Smallest
        b'\x11\xFF\xEF\xFF\xFF\xFF\xFF\xFF\xFF', b'\x11\x7F\xEF\xFF\xFF\xFF\xFF\xFF\xFF',   # Largest
        b'\x11\xc0\x09\x21\xfb\x54\x44\x2d\x18', b'\x11\x40\x09\x21\xfb\x54\x44\x2d\x18',   # PI
        b'\x11\xbf\xd5\x55\x55\x55\x55\x55\x55', b'\x11\x3f\xd5\x55\x55\x55\x55\x55\x55',   # 1/3
        b'\x11\xff\xf0\x00\x00\x00\x00\x00\x00', b'\x11\x7f\xf0\x00\x00\x00\x00\x00\x00',   # Infinity
    ],
}

test_error_single = {
    id: ['value_length_error', 'value_none', 'value_type', 'value_empty', 'exponent_error'],
    float: [b'\x08\x00\x00\x00\x00\x00', None, 0, b'', b'\x09\x00\x00\x00\x00'],
    'error': [ValueError, TypeError, TypeError, ValueError, ValueError],
}

test_error_double = {
    id: ['value_length_error', 'value_none', 'value_type', 'value_empty', 'exponent_error'],
    float: [b'\x11\x00\x00\x00\x00\x00\x00\x00', None, 0, b'', b'\x10\x00\x00\x00\x00\x00\x00\x00\x00'],
    'error': [ValueError, TypeError, TypeError, ValueError, ValueError],
}


@fixture
def negative_nan():
    return SinglePrecision(float('-nan'))


@fixture
def positive_nan():
    return SinglePrecision(float('nan'))


@fixture
def single():
    return SinglePrecision(123.456)


@fixture
def double():
    return DoublePrecision(123.456)


class TestSinglePrecision:
    # === ENCODE ===

    @mark.parametrize("value, raw_value", zip(test_data_single[float], test_data_single[bytes]), ids=test_data_single[id])
    def test_encode_raw_value(self, value, raw_value):
        assert SinglePrecision(value).raw_value == raw_value

    @mark.parametrize("value", test_data_single[float], ids=test_data_single[id])
    def test_encode_value(self, value):
        assert SinglePrecision(value).value == value

    def test_encode_negative_nan_raw_value(self, negative_nan):
        assert negative_nan.raw_value == b'\x08\xFF\xC0\x00\x00'

    def test_encode_negative_nan_value(self, negative_nan):
        assert isnan(negative_nan.value)

    def test_encode_positive_nan_raw_value(self, positive_nan):
        assert positive_nan.raw_value == b'\x08\x7F\xC0\x00\x00'

    def test_encode_positive_nan_value(self, positive_nan):
        assert isnan(positive_nan.value)

    # === DECODE ===

    @mark.parametrize("raw_value", test_data_single[bytes], ids=test_data_single[id])
    def test_decode_raw_value(self, raw_value):
        assert SinglePrecision(raw_value).raw_value == raw_value

    @mark.parametrize("value, raw_value", zip(test_data_single[float], test_data_single[bytes]), ids=test_data_single[id])
    def test_decode_value(self, value, raw_value):
        assert SinglePrecision(raw_value).value == value

    def test_decode_negative_nan_raw_value(self):
        assert SinglePrecision(b'\x08\xFF\xC0\x00\x00').raw_value == b'\x08\xFF\xC0\x00\x00'

    def test_decode_negative_nan_value(self):
        assert isnan(SinglePrecision(b'\x08\xFF\xC0\x00\x00').value)

    def test_decode_positive_nan_raw_value(self):
        assert SinglePrecision(b'\x08\x7F\xC0\x00\x00').raw_value == b'\x08\x7F\xC0\x00\x00'

    def test_decode_positive_nan_value(self, positive_nan):
        assert isnan(SinglePrecision(b'\x08\x7F\xC0\x00\x00').value)

    # === OTHER FIELDS ===

    def test_raw_tag(self, single):
        assert single.raw_tag == b'\x87'

    def test_tag(self, single):
        assert single.tag == 'SinglePrecisionFloatingPoint'

    def test_raw_length(self, single):
        assert single.raw_length == b'\x05'

    def test_length(self, single):
        assert single.length == 5

    def test_bytes(self, single):
        assert bytes(single) == b'\x87\x05\x08\x42\xF6\xE9\x79'

    def test_len(self, single):
        assert len(single) == 7

    # === EXCEPTIONS ===

    @mark.parametrize("value, error", zip(test_error_single[float], test_error_single['error']), ids=test_error_single[id])
    def test_error(self, value, error):
        with raises(error):
            SinglePrecision(value)


class TestDoublePrecision:
    # === ENCODE ===

    @mark.parametrize("value, raw_value", zip(test_data_double[float], test_data_double[bytes]), ids=test_data_double[id])
    def test_encode_raw_value(self, value, raw_value):
        assert DoublePrecision(value).raw_value == raw_value

    @mark.parametrize("value", test_data_double[float], ids=test_data_double[id])
    def test_encode_value(self, value):
        assert DoublePrecision(value).value == value

    def test_encode_negative_nan_raw_value(self, negative_nan):
        assert negative_nan.raw_value == b'\x08\xFF\xC0\x00\x00'

    def test_encode_negative_nan_value(self, negative_nan):
        assert isnan(negative_nan.value)

    def test_encode_positive_nan_raw_value(self, positive_nan):
        assert positive_nan.raw_value == b'\x08\x7F\xC0\x00\x00'

    def test_encode_positive_nan_value(self, positive_nan):
        assert isnan(positive_nan.value)

    # === DECODE ===

    @mark.parametrize("raw_value", test_data_double[bytes], ids=test_data_double[id])
    def test_decode_raw_value(self, raw_value):
        assert DoublePrecision(raw_value).raw_value == raw_value

    @mark.parametrize("value, raw_value", zip(test_data_double[float], test_data_double[bytes]), ids=test_data_double[id])
    def test_decode_value(self, value, raw_value):
        assert DoublePrecision(raw_value).value == value

    def test_decode_negative_nan_raw_value(self):
        assert DoublePrecision(b'\x11\xFF\xF8\x00\x00\x00\x00\x00\x00').raw_value == \
               b'\x11\xFF\xF8\x00\x00\x00\x00\x00\x00'

    def test_decode_negative_nan_value(self):
        assert isnan(DoublePrecision(b'\x11\xFF\xF8\x00\x00\x00\x00\x00\x00').value)

    def test_decode_positive_nan_raw_value(self):
        assert DoublePrecision(b'\x11\x7F\xF8\x00\x00\x00\x00\x00\x00').raw_value == \
               b'\x11\x7F\xF8\x00\x00\x00\x00\x00\x00'

    def test_decode_positive_nan_value(self, positive_nan):
        assert isnan(DoublePrecision(b'\x11\x7F\xF8\x00\x00\x00\x00\x00\x00').value)

    # === OTHER FIELDS ===

    def test_raw_tag(self, double):
        assert double.raw_tag == b'\x87'

    def test_tag(self, double):
        assert double.tag == 'DoublePrecisionFloatingPoint'

    def test_raw_length(self, double):
        assert double.raw_length == b'\x09'

    def test_length(self, double):
        assert double.length == 9

    def test_bytes(self, double):
        assert bytes(double) == b'\x87\x09\x11\x40\x5E\xDD\x2F\x1A\x9F\xBE\x77'

    def test_len(self, double):
        assert len(double) == 11

    # === EXCEPTIONS ===

    @mark.parametrize("value, error", zip(test_error_double[float], test_error_double['error']), ids=test_error_double[id])
    def test_error(self, value, error):
        with raises(error):
            DoublePrecision(value)
