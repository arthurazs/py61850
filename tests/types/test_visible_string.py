from pytest import fixture, raises

from py61850.types import VisibleString


@fixture
def extreme():
    return VisibleString('a' * 0xFF)


@fixture
def none():
    return VisibleString(None)


@fixture
def string():
    return VisibleString('string')


@fixture
def empty():
    return VisibleString('')


# === DECODE ===

def test_byte_string_min_raw_value():
    assert VisibleString(b'a').raw_value == b'a'


def test_byte_string_min_value():
    assert VisibleString(b'a').value == 'a'


def test_byte_string_max_raw_value():
    assert VisibleString(b'a' * 0xFF).raw_value == b'a' * 0xFF


def test_byte_string_max_value():
    assert VisibleString(b'a' * 0xFF).value == 'a' * 0xFF


# === NONE ===

def test_none_raw_value(none):
    assert none.raw_value is None


def test_none_value(none):
    assert none.value is None


def test_none_raw_length(none):
    assert none.raw_length == b'\x00'


def test_none_length(none):
    assert none.length == 0


def test_none_bytes(none):
    assert bytes(none) == b'\x8A\x00'


def test_none_len(none):
    assert len(none) == 2


# === EMPTY ===

def test_empty_raw_value(empty):
    assert empty.raw_value is None


def test_empty_value(empty):
    assert empty.value is None


def test_empty_raw_length(empty):
    assert empty.raw_length == b'\x00'


def test_empty_length(empty):
    assert empty.length == 0


def test_empty_bytes(empty):
    assert bytes(empty) == b'\x8A\x00'


def test_empty_len(empty):
    assert len(empty) == 2


# === REGULAR VALUES ===

def test_raw_tag(string):
    assert string.raw_tag == b'\x8A'


def test_tag(string):
    assert string.tag == 'VisibleString'


def test_raw_length(string):
    assert string.raw_length == b'\x06'


def test_length(string):
    assert string.length == 6


def test_bytes(string):
    assert bytes(string) == b'\x8A\x06string'


def test_len(string):
    assert len(string) == 8


# === EXTREME VALUES ===

def test_extreme_raw_length(extreme):
    assert extreme.raw_length == b'\x81\xFF'


def test_extreme_length(extreme):
    assert extreme.length == 0xFF


def test_extreme_bytes(extreme):
    assert bytes(extreme) == b'\x8A\x81\xFF' + (b'a' * 0xFF)


def test_extreme_len(extreme):
    assert len(extreme) == 3 + 0xFF


# === EXCEPTIONS ===

def test_encode_decode():
    with raises(TypeError):
        VisibleString(1)


def test_encode_above():
    with raises(ValueError):
        VisibleString('a' * 0x1FF)


def test_decode_below():
    with raises(ValueError):
        VisibleString(b'')


def test_decode_above():
    with raises(ValueError):
        VisibleString(b'a' * 0x1FF)
