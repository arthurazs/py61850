from struct import pack as s_pack

from py61850.utils.errors import raise_type


def int_u16(integer: int, min_range: int = 0, max_range: int = 0xFFFF) -> bytes:
    if isinstance(integer, int):
        if min_range <= integer <= max_range:
            return s_pack('!H', integer)
        raise ValueError('integer out of supported range')
    raise_type('integer', int, type(integer))


def u16_str(byte_stream: bytes) -> str:
    if isinstance(byte_stream, bytes):
        if len(byte_stream) == 2:
            return byte_stream.hex().upper()
        raise ValueError('byte_stream out of supported length')
    raise_type('byte_stream', bytes, type(byte_stream))
