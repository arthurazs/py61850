from pytest import raises
from pytest import mark

from iec.types.integer import Signed, Unsigned


class TestSigned:
    S_DATA = {
        id: [
            '1_min', '1_max',
            '2_min', '2_max',
            '4_min', '4_max',
            '8_min', '8_max',
        ],
        int: [
            -0x80, 0x7F,                        # 1 min/max
            -0x8000, 0x7FFF,                    # 2 min/max
            -0x80000000, 0x7FFFFFFF,            # 4 min/max
            -0x80 ** 0x9, (0x80 ** 0x9) - 1,    # 8 min/max
        ],
        bytes: [
            b'\x80', b'\x7F',                                                           # 1 min/max
            b'\x80\x00', b'\x7F\xFF',                                                   # 2 min/max
            b'\x80\x00\x00\x00', b'\x7F\xFF\xFF\xFF',                                   # 4 min/max
            b'\x80\x00\x00\x00\x00\x00\x00\x00', b'\x7F\xFF\xFF\xFF\xFF\xFF\xFF\xFF',   # 8 min/max
        ],
    }

    S_ERROR = {
        id: ['value_range_error', 'value_none', 'value_type', 'value_empty'],
        int: [0x80 ** 0x9, None, '1', b''],
        'error': [ValueError, TypeError, TypeError, ValueError],
    }

    S_FIELDS = {
        id: ['regular', 'extreme'],
        int: [0x13, -0x7F ** 0x8],
        'raw_length': [b'\x01', b'\x08'],
        'length': [1, 8],
        bytes: [b'\x85\x01\x13', b'\x85\x08\xFF\x0F\x91\xBB\xA6\xF9\x03\xFF'],
        len: [3, 10],
    }

    # === ENCODE ===

    @mark.parametrize("value, raw_value", zip(S_DATA[int], S_DATA[bytes]), ids=S_DATA[id])
    def test_encode_raw_value(self, value, raw_value):
        assert Signed(value).raw_value == raw_value

    @mark.parametrize("value", S_DATA[int], ids=S_DATA[id])
    def test_encode_value(self, value):
        assert Signed(value).value == value

    # === DECODE ===

    @mark.parametrize("raw_value", S_DATA[bytes], ids=S_DATA[id])
    def test_decode_raw_value(self, raw_value):
        assert Signed(raw_value).raw_value == raw_value

    @mark.parametrize("value, raw_value", zip(S_DATA[int], S_DATA[bytes]), ids=S_DATA[id])
    def test_decode_value(self, value, raw_value):
        assert Signed(raw_value).value == value

    # === OTHER FIELDS ===

    @mark.parametrize("value", S_FIELDS[int], ids=S_FIELDS[id])
    def test_raw_tag(self, value):
        assert Signed(value).raw_tag == b'\x85'

    @mark.parametrize("value", S_FIELDS[int], ids=S_FIELDS[id])
    def test_tag(self, value):
        assert Signed(value).tag == 'SignedInteger'

    @mark.parametrize("value, expected", zip(S_FIELDS[int], S_FIELDS['raw_length']), ids=S_FIELDS[id])
    def test_raw_length(self, value, expected):
        assert Signed(value).raw_length == expected

    @mark.parametrize("value, expected", zip(S_FIELDS[int], S_FIELDS['length']), ids=S_FIELDS[id])
    def test_length(self, value, expected):
        assert Signed(value).length == expected

    @mark.parametrize("value, expected", zip(S_FIELDS[int], S_FIELDS[bytes]), ids=S_FIELDS[id])
    def test_bytes(self, value, expected):
        assert bytes(Signed(value)) == expected

    @mark.parametrize("value, expected", zip(S_FIELDS[int], S_FIELDS[len]), ids=S_FIELDS[id])
    def test_len(self, value, expected):
        assert len(Signed(value)) == expected

    # === EXCEPTIONS ===

    @mark.parametrize("value, error", zip(S_ERROR[int], S_ERROR['error']), ids=S_ERROR[id])
    def test_error(self, value, error):
        with raises(error):
            Signed(value)


class TestUnsigned:
    U_DATA = {
        id: [
            '1_min', '1_max',
            '2_min', '2_max',
            '4_min', '4_max',
        ],
        int: [
            0, 0xFF,
            0x1FF, 0xFFFF,
            0x1FFFF, 0xFFFFFFFF,
        ],
        bytes: [
            b'\x00', b'\xFF',
            b'\x01\xFF', b'\xFF\xFF',
            b'\x00\x01\xFF\xFF', b'\xFF\xFF\xFF\xFF',
        ],
    }

    U_ERROR = {
        id: ['value_range_below', 'value_range_above', 'value_none', 'value_type', 'value_empty'],
        int: [-1, 0x1FFFFFFFF, None, '1', b''],
        'error': [ValueError, ValueError, TypeError, TypeError, ValueError],
    }

    U_FIELDS = {
        id: ['regular', 'extreme'],
        int: [0x13, 0x131313],
        'raw_length': [b'\x01', b'\x04'],
        'length': [1, 4],
        bytes: [b'\x86\x01\x13', b'\x86\x04\x00\x13\x13\x13'],
        len: [3, 6],
    }

    # === ENCODE ===

    @mark.parametrize("value, raw_value", zip(U_DATA[int], U_DATA[bytes]), ids=U_DATA[id])
    def test_encode_raw_value(self, value, raw_value):
        assert Unsigned(value).raw_value == raw_value

    @mark.parametrize("value", U_DATA[int], ids=U_DATA[id])
    def test_encode_value(self, value):
        assert Unsigned(value).value == value

    # === DECODE ===

    @mark.parametrize("raw_value", U_DATA[bytes], ids=U_DATA[id])
    def test_decode_raw_value(self, raw_value):
        assert Unsigned(raw_value).raw_value == raw_value

    @mark.parametrize("value, raw_value", zip(U_DATA[int], U_DATA[bytes]), ids=U_DATA[id])
    def test_decode_value(self, value, raw_value):
        assert Unsigned(raw_value).value == value

    # === OTHER FIELDS ===

    @mark.parametrize("value", U_FIELDS[int], ids=U_FIELDS[id])
    def test_raw_tag(self, value):
        assert Unsigned(value).raw_tag == b'\x86'

    @mark.parametrize("value", U_FIELDS[int], ids=U_FIELDS[id])
    def test_tag(self, value):
        assert Unsigned(value).tag == 'UnsignedInteger'

    @mark.parametrize("value, expected", zip(U_FIELDS[int], U_FIELDS['raw_length']), ids=U_FIELDS[id])
    def test_raw_length(self, value, expected):
        assert Unsigned(value).raw_length == expected

    @mark.parametrize("value, expected", zip(U_FIELDS[int], U_FIELDS['length']), ids=U_FIELDS[id])
    def test_length(self, value, expected):
        assert Unsigned(value).length == expected

    @mark.parametrize("value, expected", zip(U_FIELDS[int], U_FIELDS[bytes]), ids=U_FIELDS[id])
    def test_bytes(self, value, expected):
        assert bytes(Unsigned(value)) == expected

    @mark.parametrize("value, expected", zip(U_FIELDS[int], U_FIELDS[len]), ids=U_FIELDS[id])
    def test_len(self, value, expected):
        assert len(Unsigned(value)) == expected

    # === EXCEPTIONS ===

    @mark.parametrize("value, error", zip(U_ERROR[int], U_ERROR['error']), ids=U_ERROR[id])
    def test_error(self, value, error):
        with raises(error):
            Unsigned(value)
