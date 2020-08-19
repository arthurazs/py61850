from typing import Optional, Union

from iec.types.base import Base
from utils.errors import raise_type


class VisibleString(Base):

    def __init__(self, value: Union[str, bytes]) -> None:
        raw_value, value = self._parse_value(value)
        super().__init__(raw_tag=b'\x8A', raw_value=raw_value)
        self._value = value

    @staticmethod
    def _encode_value(value: Optional[str]) -> Optional[bytes]:
        if value is None:
            return None
        elif isinstance(value, str):
            if len(value) == 0:
                return None
            elif 0 < len(value) <= 0xFF:
                # TODO How should I limit other string lengths?
                return value.encode('utf8')
        raise_type('value', str, type(value))

    @staticmethod
    def _decode_value(value: bytes) -> Optional[str]:
        if isinstance(value, bytes):
            if 0 < len(value) <= 0xFF:
                return value.decode('utf8')
            raise ValueError('value out of supported length')
        raise_type('value', bytes, type(value))
