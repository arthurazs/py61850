from pytest import fixture, raises
from pytest import mark
from iec.types.unsigned_integer import UnsignedInteger

test_data = {
    id: [
        '1_min',
        '1_max',
        '2_min',
        '2_max',
        '4_min',
        '4_max',
    ],
    int: [
        0,
        0xFF,
        0x1FF,
        0xFFFF,
        0x1FFFF,
        0xFFFFFFFF,
    ],
    bytes: [
        b'\x00',
        b'\xFF',
        b'\x01\xFF',
        b'\xFF\xFF',
        b'\x00\x01\xFF\xFF',
        b'\xFF\xFF\xFF\xFF',
    ],
}

test_error_data = {
    id: [
        'value_range_below',
        'value_range_above',
        'value_none',
        'value_type',
        'value_empty',
    ],
    int: [
        -1,
        0x1FFFFFFFF,
        None,
        '1',
        b'',
    ],
    'error': [
        ValueError,
        ValueError,
        TypeError,
        TypeError,
        ValueError,
    ],
}

test_fields = {
    id: [
        'regular',
        'extreme',
    ],
    int: [
        0x13,
        0x131313,
    ],
    'raw_length': [
        b'\x01',
        b'\x04',
    ],
    'length': [
        1,
        4,
    ],
    bytes: [
        b'\x86\x01\x13',
        b'\x86\x04\x00\x13\x13\x13',
    ],
    len: [
        3,
        6,
    ],
}


@fixture
def regular():
    return UnsignedInteger(13)


@fixture
def extreme():
    return UnsignedInteger(0x131313)


# === ENCODE ===

@mark.parametrize("value, raw_value", zip(test_data[int], test_data[bytes]), ids=test_data[id])
def test_encode_raw_value(value, raw_value):
    assert UnsignedInteger(value).raw_value == raw_value


@mark.parametrize("value", test_data[int], ids=test_data[id])
def test_encode_value(value):
    assert UnsignedInteger(value).value == value


# === DECODE ===

@mark.parametrize("raw_value", test_data[bytes], ids=test_data[id])
def test_decode_raw_value(raw_value):
    assert UnsignedInteger(raw_value).raw_value == raw_value


@mark.parametrize("value, raw_value", zip(test_data[int], test_data[bytes]), ids=test_data[id])
def test_decode_value(value, raw_value):
    assert UnsignedInteger(raw_value).value == value


# === OTHER FIELDS ===

@mark.parametrize("value", test_fields[int], ids=test_fields[id])
def test_raw_tag(value):
    assert UnsignedInteger(value).raw_tag == b'\x86'


@mark.parametrize("value", test_fields[int], ids=test_fields[id])
def test_tag(value):
    assert UnsignedInteger(value).tag == 'UnsignedInteger'


@mark.parametrize("value, expected", zip(test_fields[int], test_fields['raw_length']), ids=test_fields[id])
def test_raw_length(value, expected):
    assert UnsignedInteger(value).raw_length == expected


@mark.parametrize("value, expected", zip(test_fields[int], test_fields['length']), ids=test_fields[id])
def test_length(value, expected):
    assert UnsignedInteger(value).length == expected


@mark.parametrize("value, expected", zip(test_fields[int], test_fields[bytes]), ids=test_fields[id])
def test_bytes(value, expected):
    assert bytes(UnsignedInteger(value)) == expected


@mark.parametrize("value, expected", zip(test_fields[int], test_fields[len]), ids=test_fields[id])
def test_len(value, expected):
    assert len(UnsignedInteger(value)) == expected


# === EXCEPTIONS ===

@mark.parametrize("value, error", zip(test_error_data[int], test_error_data['error']), ids=test_error_data[id])
def test_error(value, error):
    with raises(error):
        UnsignedInteger(value)
