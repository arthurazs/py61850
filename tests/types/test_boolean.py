from pytest import fixture, raises

from py61850.types import Boolean


@fixture
def true():
    return Boolean(True)


# === DECODE ===

def test_byte_true_min_raw_value():
    assert Boolean(b'\x01').raw_value == b'\x01'


def test_byte_true_min_value():
    assert Boolean(b'\x01').value is True


def test_byte_true_max_raw_value():
    assert Boolean(b'\xFF').raw_value == b'\xFF'


def test_byte_true_max_value():
    assert Boolean(b'\xFF').value is True


def test_byte_false_raw_value():
    assert Boolean(b'\x00').raw_value == b'\x00'


def test_byte_false_value():
    assert Boolean(b'\x00').value is False


# === TRUE ===

def test_true_value(true):
    assert true.value is True


def test_true_raw_value(true):
    assert true.raw_value != b'\x00'


# === FALSE ===

def test_false_value():
    assert Boolean(False).value is False


def test_false_raw_value(true):
    assert Boolean(False).raw_value == b'\x00'


# === UNCHANGED VALUES ===

def test_raw_tag(true):
    assert true.raw_tag == b'\x83'


def test_tag(true):
    assert true.tag == 'Boolean'


def test_raw_length(true):
    assert true.raw_length == b'\x01'


def test_length(true):
    assert true.length == 1


def test_bytes():
    assert bytes(Boolean(False)) == b'\x83\x01\x00'


def test_len(true):
    assert len(true) == 3


# === EXCEPTIONS ===

def test_encode_decode():
    with raises(TypeError):
        Boolean(1)


def test_decode_below():
    with raises(ValueError):
        Boolean(b'')


def test_decode_above():
    with raises(ValueError):
        Boolean(b'\x00\x00')


def test_none():
    with raises(TypeError):
        Boolean(None)
