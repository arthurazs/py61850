from struct import pack as s_pack, unpack as s_unpack
from typing import Union

from py61850.types.base import Base
from py61850.utils.errors import raise_type


class Unsigned(Base):
    def __init__(self, value: Union[int, bytes]) -> None:
        raw_value, value = self._parse_value(value)
        super().__init__(raw_tag=b'\x86', raw_value=raw_value)
        self._value = value

    @staticmethod
    def _encode_value(value: int) -> bytes:
        if isinstance(value, int):
            if value < 0:
                raise ValueError('Unsigned integer cannot be negative')
            elif value <= 0xFF:
                return s_pack('!B', value)
            elif value <= 0xFFFF:
                return s_pack('!H', value)
            # elif value <= 0xFFFFFF:
            #     # NOTE regular MMS does not have 24 bits unsigned int
            #     # NOTE 24 bits unsigned int seems to be used only for timestamp
            #     return s_pack('!I', value)[1:]
            elif value <= 0xFFFFFFFF:
                return s_pack('!I', value)
            raise ValueError('Unsigned integer out of supported range')
        raise_type('value', int, type(value))

    @staticmethod
    def _decode_value(value: bytes) -> int:
        if isinstance(value, bytes):
            if len(value) == 1:
                return s_unpack('!B', value)[0]
            elif len(value) == 2:
                return s_unpack('!H', value)[0]
            # elif len(value) == 3:
            #     # NOTE regular MMS does not have 24 bits unsigned int
            #     # NOTE 24 bits unsigned int seems to be used only for timestamp
            #     return s_unpack('!I', b'\x00' + value)[0]
            elif len(value) == 4:
                return s_unpack('!I', value)[0]
            raise ValueError('Unsigned integer out of supported range')
        raise_type('value', bytes, type(value))

    @property
    def tag(self) -> str:
        """The class name."""
        return self.__class__.__name__ + 'Integer'


class Signed(Base):
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

    @property
    def tag(self) -> str:
        """The class name."""
        return self.__class__.__name__ + 'Integer'
