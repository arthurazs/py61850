from pytest import fixture, raises
from pytest import mark

from iec.types.signed_integer import SignedInteger

test_data = {
    id: ['1_min', '1_max', '2_min', '2_max', '4_min', '4_max', '8_min', '8_max'],
    int: [
        -0x80,                                  # 1_min
        0x7F,                                   # 1_max
        -0x8000,                                # 2_min
        0x7FFF,                                 # 2_max
        -0x80000000,                            # 4_min
        0x7FFFFFFF,                             # 4_max
        -0x80 ** 0x9,                           # 8_min
        (0x80 ** 0x9) - 1,                      # 8_max
    ],
    bytes: [
        b'\x80',                                # 1_min
        b'\x7F',                                # 1_max
        b'\x80\x00',                            # 2_min
        b'\x7F\xFF',                            # 2_max
        b'\x80\x00\x00\x00',                    # 4_min
        b'\x7F\xFF\xFF\xFF',                    # 4_max
        b'\x80\x00\x00\x00\x00\x00\x00\x00',    # 8_min
        b'\x7F\xFF\xFF\xFF\xFF\xFF\xFF\xFF',    # 8_max
    ],
}

test_error_data = {
    id: ['value_range_error', 'value_none', 'value_type', 'value_empty'],
    int: [0x80 ** 0x9, None, '1', b''],
    'error': [ValueError, TypeError, TypeError, ValueError],
}

test_fields = {
    id: ['regular', 'extreme'],
    int: [0x13, -0x7F ** 0x8],
    'raw_length': [b'\x01', b'\x08'],
    'length': [1, 8],
    bytes: [b'\x85\x01\x13', b'\x85\x08\xFF\x0F\x91\xBB\xA6\xF9\x03\xFF'],
    len: [3, 10],
}


# === ENCODE ===

@mark.parametrize("value, raw_value", zip(test_data[int], test_data[bytes]), ids=test_data[id])
def test_encode_raw_value(value, raw_value):
    assert SignedInteger(value).raw_value == raw_value


@mark.parametrize("value", test_data[int], ids=test_data[id])
def test_encode_value(value):
    assert SignedInteger(value).value == value


# === DECODE ===

@mark.parametrize("raw_value", test_data[bytes], ids=test_data[id])
def test_decode_raw_value(raw_value):
    assert SignedInteger(raw_value).raw_value == raw_value


@mark.parametrize("value, raw_value", zip(test_data[int], test_data[bytes]), ids=test_data[id])
def test_decode_value(value, raw_value):
    assert SignedInteger(raw_value).value == value


# === OTHER FIELDS ===

@mark.parametrize("value", test_fields[int], ids=test_fields[id])
def test_raw_tag(value):
    assert SignedInteger(value).raw_tag == b'\x85'


@mark.parametrize("value", test_fields[int], ids=test_fields[id])
def test_tag(value):
    assert SignedInteger(value).tag == 'SignedInteger'


@mark.parametrize("value, expected", zip(test_fields[int], test_fields['raw_length']), ids=test_fields[id])
def test_raw_length(value, expected):
    assert SignedInteger(value).raw_length == expected


@mark.parametrize("value, expected", zip(test_fields[int], test_fields['length']), ids=test_fields[id])
def test_length(value, expected):
    assert SignedInteger(value).length == expected


@mark.parametrize("value, expected", zip(test_fields[int], test_fields[bytes]), ids=test_fields[id])
def test_bytes(value, expected):
    assert bytes(SignedInteger(value)) == expected


@mark.parametrize("value, expected", zip(test_fields[int], test_fields[len]), ids=test_fields[id])
def test_len(value, expected):
    assert len(SignedInteger(value)) == expected


# === EXCEPTIONS ===

@mark.parametrize("value, error", zip(test_error_data[int], test_error_data['error']), ids=test_error_data[id])
def test_error(value, error):
    with raises(error):
        SignedInteger(value)
