from typing import Union

from py61850.types.base import Base
from py61850.utils.errors import raise_type


class Boolean(Base):

    def __init__(self, value: Union[bool, bytes]) -> None:
        raw_value, value = self._parse_value(value)
        super().__init__(raw_tag=b'\x83', raw_value=raw_value)
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
