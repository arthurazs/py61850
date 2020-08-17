from pytest import fixture, raises
from iec.types.base import Base


@fixture
def empty_value():
    return Base(b'\x80')


@fixture
def generic():
    return Base(b'\x81', b'string')


# === EMPTY VALUE ===

def test_empty_value_raw_tag(empty_value):
    assert empty_value.raw_tag == b'\x80'


def test_empty_value_tag(empty_value):
    assert empty_value.tag == '80'


def test_empty_value_raw_value(empty_value):
    assert empty_value.raw_value is None


def test_empty_value_raw_length(empty_value):
    assert empty_value.raw_length == b'\x00'


def test_empty_value_length(empty_value):
    assert empty_value.length == 0


def test_empty_value_len(empty_value):
    assert len(empty_value) == 2


def test_empty_value_bytes(empty_value):
    assert bytes(empty_value) == b'\x80\x00'


# === GENERIC ===

def test_generic_raw_tag(generic):
    assert generic.raw_tag == b'\x81'


def test_generic_tag(generic):
    assert generic.tag == '81'


def test_generic_raw_value(generic):
    assert generic.raw_value == b'string'


def test_generic_raw_length(generic):
    assert generic.raw_length == b'\x06'


def test_generic_length(generic):
    assert generic.length == 6


def test_generic_len(generic):
    assert len(generic) == 8


def test_generic_bytes(generic):
    assert bytes(generic) == b'\x81\x06string'


# === SET LENGTH ===

def test_set_length_0_max_raw():
    base = Base(b'\x82', b'a' * 0x79)
    assert base.raw_length == b'\x79'


def test_set_length_0_max():
    base = Base(b'\x82', b'a' * 0x79)
    assert base.length == 0x79


def test_set_length_1_min_raw():
    base = Base(b'\x82', b'a' * 0x80)
    assert base.raw_length == b'\x81\x80'


def test_set_length_1_min():
    base = Base(b'\x82', b'a' * 0x80)
    assert base.length == 0x80


def test_set_length_1_max_raw():
    base = Base(b'\x82', b'a' * 0xFF)
    assert base.raw_length == b'\x81\xFF'


def test_set_length_1_max():
    base = Base(b'\x82', b'a' * 0xFF)
    assert base.length == 0xFF


def test_set_length_2_min_raw():
    base = Base(b'\x82', b'a' * 0x1FF)
    assert base.raw_length == b'\x82\x01\xFF'


def test_set_length_2_min():
    base = Base(b'\x82', b'a' * 0x1FF)
    assert base.length == 0x1FF


def test_set_length_2_max_raw():
    base = Base(b'\x82', b'a' * 0xFFFF)
    assert base.raw_length == b'\x82\xFF\xFF'


def test_set_length_2_max():
    base = Base(b'\x82', b'a' * 0xFFFF)
    assert base.length == 0xFFFF


# === EXCEPTIONS ===

def test_set_tag_value_error_below():
    with raises(ValueError):
        Base(b'')


def test_set_tag_value_error_above():
    with raises(ValueError):
        Base(b'\x00\x00')


def test_set_tag_type_error():
    with raises(TypeError):
        Base('\x83')


def test_set_raw_value_type_error():
    with raises(TypeError):
        Base(b'\x84', 'string')


def test_set_length_value_error():
    with raises(ValueError):
        Base(b'\x85', b'a' * 0x1FFFF)
