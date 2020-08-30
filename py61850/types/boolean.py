from typing import Union

from py61850.types.base import Base
from py61850.utils.errors import raise_type


class Boolean(Base):

    def __init__(self, anything: Union[bool, bytes], raw_tag: bytes = b'\x83') -> None:
        raw_value, value = self._parse(anything)
        super().__init__(raw_tag=raw_tag, raw_value=raw_value)
        self._value = value

    @staticmethod
    def _encode(value: bool) -> bytes:
        if not isinstance(value, bool):
            raise_type('value', bool, type(value))
        return b'\x0F' if value else b'\x00'

    @staticmethod
    def _decode(raw_value: bytes) -> bool:
        if len(raw_value) != 1:
            raise ValueError('value out of supported length')
        return raw_value != b'\x00'
