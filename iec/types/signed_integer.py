from struct import pack as s_pack, unpack as s_unpack
from typing import Union

from iec.types.base import Base
from utils.errors import raise_type


class SignedInteger(Base):
    def __init__(self, value: Union[int, bytes]) -> None:
        raw_value, value = self._parse_value(value)
        super().__init__(raw_tag=b'\x85', raw_value=raw_value)
        self._value = value

    @staticmethod
    def _encode_value(value: int) -> bytes:
        if isinstance(value, int):
            if -0x80 <= value < 0x80:
                return s_pack('!b', value)
            elif -0x8000 <= value < 0x8000:
                return s_pack('!h', value)
            elif -0x80000000 <= value < 0x80000000:
                return s_pack('!i', value)
            elif -0x80 ** 0x9 <= value < 0x80 ** 0x9:  # NOTE change support from 64 to 128?
                return s_pack('!q', value)
            raise ValueError('Signed integer out of supported range')
        raise_type('value', int, type(value))

    @staticmethod
    def _decode_value(value: bytes) -> int:
        if isinstance(value, bytes):
            if len(value) == 1:
                return s_unpack('!b', value)[0]
            elif len(value) == 2:
                return s_unpack('!h', value)[0]
            elif len(value) == 4:
                return s_unpack('!i', value)[0]
            elif len(value) == 8:
                return s_unpack('!q', value)[0]
            raise ValueError('Signed integer out of supported range')
        raise_type('value', bytes, type(value))
