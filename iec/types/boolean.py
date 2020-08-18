from iec.types.base import Base
from utils.errors import raise_type
from typing import Union


class Boolean(Base):

    def __init__(self, value: Union[bool, bytes]) -> None:
        try:
            raw_value = self._encode_value(value)
        except TypeError:
            raw_value = value
            value = self._decode_value(value)
        super().__init__(
            raw_tag=b'\x83',
            raw_value=raw_value)
        self._value = value

    @staticmethod
    def _encode_value(value: bool) -> bytes:
        if isinstance(value, bool):
            return b'\x0F' if value else b'\x00'
        raise_type('value', bool, type(value))

    @staticmethod
    def _decode_value(value: bytes) -> bool:
        if isinstance(value, bytes):
            if len(value) == 1:
                return value != b'\x00'
            raise ValueError('value out of supported length')
        raise_type('value', bytes, type(value))

    @property
    def value(self) -> bool:
        return self._value
