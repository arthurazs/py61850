from struct import pack as s_pack, unpack as s_unpack
from typing import Optional, Tuple, Union

from py61850.types.base import Base, Generic
from py61850.utils.errors import raise_type


class Quality(Generic):
    def __init__(self, leap_seconds_known: bool = False, clock_failure: bool = False,
                 clock_not_synchronized: bool = True, time_accuracy: int = 0, raw_value: Optional[bytes] = None):
        if raw_value is None:
            raw_value = self._encode((leap_seconds_known, clock_failure, clock_not_synchronized, time_accuracy))
        else:
            leap_seconds_known, clock_failure, clock_not_synchronized, time_accuracy = self._decode(raw_value)
        self._raw_value = raw_value
        self._leap_seconds = leap_seconds_known
        self._clock_failure = clock_failure
        self._clock_not_sync = clock_not_synchronized
        self._accuracy = time_accuracy

    def __bytes__(self):
        return self._raw_value

    def _decode(self, raw_value: bytes) -> Tuple[bool, bool, bool, int]:
        if not isinstance(raw_value, bytes):
            raise_type('raw_value', bytes, type(raw_value))
        if len(raw_value) != 1:
            raise ValueError('raw_value out of supported length')

        bits = s_unpack('!B', raw_value)[0]

        time_accuracy = bits & 0x1F
        if time_accuracy > 24 and time_accuracy != 0x1F:
            raise ValueError('bits out of supported range')

        leap_seconds_known = (bits & 0x80) == 0x80
        clock_failure = (bits & 0x40) == 0x40
        clock_not_synchronized = (bits & 0x20) == 0x20

        return leap_seconds_known, clock_failure, clock_not_synchronized, time_accuracy

    def _encode(self, value: Tuple[bool, bool, bool, int]) -> bytes:
        leap_seconds_known, clock_failure, clock_not_synchronized, time_accuracy = value
        if not isinstance(leap_seconds_known, bool):
            raise_type('leap_seconds_known', bool, type(leap_seconds_known))
        if not isinstance(clock_failure, bool):
            raise_type('clock_failure', bool, type(clock_failure))
        if not isinstance(clock_not_synchronized, bool):
            raise_type('clock_not_synchronized', bool, type(clock_not_synchronized))
        if not isinstance(time_accuracy, int):
            raise_type('time_accuracy', int, type(time_accuracy))

        if 0 <= time_accuracy <= 24 or time_accuracy == 0x1F:
            self._accuracy = time_accuracy
        else:
            raise ValueError('time_accuracy out of supported range')

        bits = (leap_seconds_known << 7) + (clock_failure << 6) + \
               (clock_not_synchronized << 5) + time_accuracy
        return s_pack('!B', bits)

    @property
    def leap_seconds_known(self):
        return self._leap_seconds

    @property
    def clock_failure(self):
        return self._clock_failure

    @property
    def clock_not_synchronized(self):
        return self._clock_not_sync

    @property
    def time_accuracy(self) -> Union[int, str]:
        return 'Unspecified' if self._accuracy == 0x1F else self._accuracy


class Timestamp(Base):

    # UTC Time
    def __init__(self, anything: Union[float, bytes], quality: Optional[Quality] = None, raw_tag: bytes = b'\x91'):
        raw_value, value = self._parse((anything, quality))
        raw_value, value, quality = self.unpack_extra_value(raw_value, value)
        super().__init__(raw_tag=raw_tag, raw_value=raw_value)
        self._value = value
        self._quality = quality

    @staticmethod
    def _encode(value: Tuple[float, Quality]) -> bytes:
        value, quality = value
        if not isinstance(value, float):
            raise_type('value', float, type(value))
        if not isinstance(quality, Quality):
            raise_type('quality', Quality, type(quality))

        seconds, fraction = map(int, str(value).split('.'))
        byte_stream = s_pack('!I', seconds)
        byte_stream += s_pack('!I', fraction)[1:]
        return byte_stream + bytes(quality)

    @staticmethod
    def _decode(raw_value: bytes) -> Tuple[float, Quality]:
        raw_value, _ = raw_value
        if len(raw_value) != 8:
            raise ValueError('raw_value out of supported length')
        seconds = s_unpack('!I', raw_value[:4])[0]
        # TODO Fraction seems to be wrong
        fraction = s_unpack('!I', b'\x00' + raw_value[4:7])[0]
        quality = Quality(raw_value=raw_value[7:8])
        return float(str(f'{seconds}.{fraction}')), quality

    @property
    def leap_seconds_known(self):
        return self._quality.leap_seconds_known

    @property
    def clock_failure(self):
        return self._quality.clock_failure

    @property
    def clock_not_synchronized(self):
        return self._quality.clock_not_synchronized

    @property
    def time_accuracy(self):
        return self._quality.time_accuracy
