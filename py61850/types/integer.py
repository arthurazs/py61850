from struct import pack as s_pack, unpack as s_unpack
from typing import Union

from py61850.types.base import Base
from py61850.utils.errors import raise_type


class Unsigned(Base):
    def __init__(self,
                 anything: Union[int, bytes], min_range: int = 0, max_range: int = 0xFFFFFFFF,
                 raw_tag: bytes = b'\x86') -> None:
        self._min_range = min_range
        self._max_range = max_range
        raw_value, value = self._parse(anything)
        super().__init__(raw_tag=raw_tag, raw_value=raw_value)
        self._value = value

    def _encode(self, value: int) -> bytes:
        if isinstance(value, int):
            if value < 0:
                raise ValueError('Unsigned integer cannot be negative')
            elif value <= 0xFF and self._min_range <= value <= self._max_range:
                return s_pack('!B', value)
            elif value <= 0xFFFF and self._min_range <= value <= self._max_range:
                return s_pack('!H', value)
            # elif value <= 0xFFFFFF and self._min_range <= value <= self._max_range:
            #     # NOTE regular MMS does not have 24 bits unsigned int
            #     # NOTE 24 bits unsigned int seems to be used only for timestamp
            #     return s_pack('!I', value)[1:]
            elif value <= 0xFFFFFFFF and self._min_range <= value <= self._max_range:
                return s_pack('!I', value)
            raise ValueError('Unsigned integer out of supported range')
        raise_type('value', int, type(value))

    @staticmethod
    def _decode(raw_value: bytes) -> int:
        if isinstance(raw_value, bytes):
            if len(raw_value) == 1:
                return s_unpack('!B', raw_value)[0]
            elif len(raw_value) == 2:
                return s_unpack('!H', raw_value)[0]
            # elif len(raw_value) == 3:
            #     # NOTE regular MMS does not have 24 bits unsigned int
            #     # NOTE 24 bits unsigned int seems to be used only for timestamp
            #     return s_unpack('!I', b'\x00' + raw_value)[0]
            elif len(raw_value) == 4:
                return s_unpack('!I', raw_value)[0]
            raise ValueError('Unsigned integer out of supported range')
        raise_type('raw_value', bytes, type(raw_value))

    @property
    def tag(self) -> str:
        """The class name."""
        return self.__class__.__name__ + 'Integer'


class Signed(Base):
    def __init__(self, anything: Union[int, bytes]) -> None:
        raw_value, value = self._parse(anything)
        super().__init__(raw_tag=b'\x85', raw_value=raw_value)
        self._value = value

    @staticmethod
    def _encode(value: int) -> bytes:
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
    def _decode(raw_value: bytes) -> int:
        if isinstance(raw_value, bytes):
            if len(raw_value) == 1:
                return s_unpack('!b', raw_value)[0]
            elif len(raw_value) == 2:
                return s_unpack('!h', raw_value)[0]
            elif len(raw_value) == 4:
                return s_unpack('!i', raw_value)[0]
            elif len(raw_value) == 8:
                return s_unpack('!q', raw_value)[0]
            raise ValueError('Signed integer out of supported range')
        raise_type('raw_value', bytes, type(raw_value))

    @property
    def tag(self) -> str:
        """The class name."""
        return self.__class__.__name__ + 'Integer'
