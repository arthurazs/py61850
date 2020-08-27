from typing import Optional, Union

from py61850.types.base import Base
from py61850.utils.errors import raise_type


class VisibleString(Base):

    def __init__(self, anything: Union[str, bytes], max_length: int = 0xFF, raw_tag: bytes = b'\x8A') -> None:
        self._max_length = max_length
        raw_value, value = self._parse(anything)
        super().__init__(raw_tag=raw_tag, raw_value=raw_value)
        self._value = value

    def _encode(self, value: Optional[str]) -> Optional[bytes]:
        if value is None:
            return None
        elif isinstance(value, str):
            if len(value) == 0:
                return None
            elif 0 < len(value) <= self._max_length:
                # TODO How should I limit other string lengths?
                return value.encode('utf8')
        raise_type('value', str, type(value))

    def _decode(self, raw_value: bytes) -> Optional[str]:
        if isinstance(raw_value, bytes):
            if 0 < len(raw_value) <= self._max_length:
                return raw_value.decode('utf8')
            raise ValueError('raw_value out of supported length')
        raise_type('raw_value', bytes, type(raw_value))
