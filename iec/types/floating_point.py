from struct import pack as s_pack, unpack as s_unpack
from typing import Union

from iec.types.base import Base
from utils.errors import raise_type


class SinglePrecision(Base):
    def __init__(self, value: Union[float, bytes]) -> None:
        raw_value, value = self._parse_value(value)
        super().__init__(raw_tag=b'\x87', raw_value=raw_value)
        self._value = value

    @staticmethod
    def _encode_value(value: float) -> bytes:
        if isinstance(value, float):
            return b'\x08' + s_pack('!f', value)
        raise_type('value', float, type(value))

    @staticmethod
    def _decode_value(value: bytes) -> float:
        if isinstance(value, bytes):
            if len(value) == 5:
                if value[0:1] == b'\x08':
                    return s_unpack('!f', value[1:5])[0]
                raise ValueError("Single precision floating point's exponent out of supported range")
            raise ValueError('Single precision floating point out of supported length')
        raise_type('value', bytes, type(value))

    @property
    def tag(self) -> str:
        """The class name."""
        return 'SinglePrecisionFloatingPoint'


class DoublePrecision(Base):
    def __init__(self, value: Union[float, bytes]) -> None:
        raw_value, value = self._parse_value(value)
        super().__init__(raw_tag=b'\x87', raw_value=raw_value)
        self._value = value

    @staticmethod
    def _encode_value(value: float) -> bytes:
        if isinstance(value, float):
            return b'\x11' + s_pack('!d', value)
        raise_type('value', float, type(value))

    @staticmethod
    def _decode_value(value: bytes) -> float:
        if isinstance(value, bytes):
            if len(value) == 9:
                if value[0:1] == b'\x11':
                    return s_unpack('!d', value[1:9])[0]
                raise ValueError("Single precision floating point's exponent out of supported range")
            raise ValueError('Single precision floating point out of supported length')
        raise_type('value', bytes, type(value))

    @property
    def tag(self) -> str:
        """The class name."""
        return 'DoublePrecisionFloatingPoint'
