from struct import pack as s_pack, unpack as s_unpack
from typing import Union

from py61850.types.base import Base
from py61850.utils.errors import raise_type


class FloatingPoint(Base):
    def __init__(self, anything: Union[float, bytes], double_precision: bool) -> None:
        if double_precision:
            self._exponent = b'\x11'
            self._format = '!d'
            self._length = 9
            self._name = 'DoublePrecision'
        else:
            self._exponent = b'\x08'
            self._format = '!f'
            self._length = 5
            self._name = 'SinglePrecision'
        raw_value, value = self._parse(anything)
        super().__init__(raw_tag=b'\x87', raw_value=raw_value)
        self._value = value

    def _encode(self, value: float) -> bytes:
        if not isinstance(value, float):
            raise_type('value', float, type(value))
        return self._exponent + s_pack(self._format, value)

    def _decode(self, raw_value: bytes) -> float:
        if len(raw_value) != self._length:
            raise ValueError(f'{self._name} floating point out of supported length')
        if raw_value[0:1] != self._exponent:
            raise ValueError(f"{self._name} floating point's exponent out of supported range")
        return s_unpack(self._format, raw_value[1:self._length])[0]

    @property
    def tag(self) -> str:
        """The class name."""
        return self.__class__.__name__ + 'FloatingPoint'


class SinglePrecision(FloatingPoint):
    def __init__(self, value: Union[float, bytes]) -> None:
        super().__init__(value, double_precision=False)


class DoublePrecision(FloatingPoint):
    def __init__(self, value: Union[float, bytes]) -> None:
        super().__init__(value, double_precision=True)
