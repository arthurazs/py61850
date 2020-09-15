from abc import ABC
from typing import Any, Optional, Tuple, Union
from struct import pack as s_pack

from py61850.utils.errors import raise_type


class Generic(ABC):

    def _parse(self, anything: Any) -> Tuple[Optional[bytes], Any]:

        unpacked = anything
        if not isinstance(anything, bytes):
            try:
                unpacked = anything[0]
            except (TypeError, IndexError):
                pass

        if isinstance(unpacked, bytes):
            raw_value = anything
            value = self._decode(raw_value)
        else:
            value = anything
            raw_value = self._encode(value)
        if raw_value is None or value is None:
            return None, None
        return raw_value, value

    @staticmethod
    def _encode(value: Any) -> bytes:
        raise NotImplementedError  # pragma: no cover

    @staticmethod
    def _decode(raw_value: bytes) -> Any:
        raise NotImplementedError  # pragma: no cover


class Base(Generic, ABC):
    """This is the base for any IEC data type.

    This class does not care for encoding, nor decoding the value field,
    which should be handled by the subclass.
    Thus, the `Base` expects the already encoded value field, but handles
    the encoding/decoding of both tag and length field.

    Args:
        raw_tag: The encoded tag field.
        raw_value: The encoded value field.

    Raises:
        TypeError: If `raw_tag` type is different from `bytes`.
        TypeError: If `raw_value` type is different from `bytes` and `NoneType`.
        ValueError: If `raw_tag` length is different from 1.
    """

    def __init__(self, raw_tag: bytes, raw_value: Optional[bytes] = None) -> None:
        self._set_tag(raw_tag)
        self._set_raw_value(raw_value)
        self._parent = None

    def __bytes__(self) -> bytes:
        """Return the encoded data, including all existing fields.

        If value field is `None`: return tag + length.

        If value field is not `None`: return tag + length + value.
        """
        if self._raw_value is None:
            return self._raw_tag + self._raw_length
        return self._raw_tag + self._raw_length + self._raw_value

    def __len__(self) -> int:
        """Return the length of the encoded data, including all existing fields.

        If value field is `None`: return tag + length.

        If value field is not `None`: return tag + length + value.

        Note:
            For the length field, use the `length` property.
        """
        if self.raw_value is None:
            return len(self.raw_tag) + len(self.raw_length)
        return len(self.raw_tag) + len(self.raw_length) + len(self.raw_value)

    def set_parent(self, parent: 'Base'):
        if not isinstance(parent, Base):
            raise_type('parent', Base, type(parent))
        self._parent = parent

    def _update(self, caller: 'Base'):
        byte_stream = b''
        for value in self._value:
            byte_stream += bytes(value)
        self._set_raw_value(byte_stream)

    def _set_tag(self, raw_tag: bytes) -> None:
        # assert `raw_tag` is `bytes` and has length of 1, then set `raw_tag` and `tag`
        if not isinstance(raw_tag, bytes):
            raise_type('raw_tag', bytes, type(raw_tag))
        if len(raw_tag) != 1:
            raise ValueError('raw_tag out of supported length')
        self._raw_tag = raw_tag
        # self._tag = raw_tag.hex()
        self._tag = self.__class__.__name__

    @staticmethod
    def unpack_extra_value(value_a: Union[bytes, Tuple[bytes, Any]],
                           value_b: Union[Any, Tuple[Any, Any]]) -> Tuple[bytes, Any, Any]:
        try:
            value_a, value_c = value_a
        except ValueError:
            value_b, value_c = value_b
        if value_c is None:
            value_b, value_c = value_b
        return value_a, value_b, value_c

    @property
    def tag(self) -> str:
        """The class name."""
        return self._tag

    @property
    def raw_tag(self) -> bytes:
        """The encoded tag field."""
        return self._raw_tag

    def _set_length(self, length: int) -> None:
        """Encode length according to ASN.1 BER.

        `raw_length` will be of 1 byte long if < 128.
        If it's 2+ bytes long, the first byte indicates how many
        bytes follows.

        Example:
            128 == b'\x81\x80', where 0x81 indicates 1 extra byte
            for the length, and 0x80 is the length itself.

        Args:
            length: The length to be encoded.

        Raises:
            ValueError: If `length` is greater than `0xFFFF`.
        """
        # NOTE enable extra_length > 2?
        # NOTE indefinite length?
        if 0 <= length < 0x80:
            self._raw_length = s_pack('!B', length)
        elif 0x80 <= length <= 0xFF:
            self._raw_length = s_pack('!BB', 0x81, length)
        elif 0xFF < length <= 0xFFFF:
            self._raw_length = s_pack('!BH', 0x82, length)
        else:
            raise ValueError(f'data length greater than {0xFFFF}')
        self._length = length

    @property
    def raw_value(self) -> Optional[bytes]:
        """The encoded value field."""
        return self._raw_value

    def _set_raw_value(self, raw_value: Optional[bytes]) -> None:
        """Set raw value field.

        Note:
            This method does not encode the value field.
            This should be done by the subclass using
            the `_encode_value()` method.

        Args:
            raw_value: The raw value to be set.

        Raises:
            ValueError: If the length of `raw_value` is greater than `0xFFFF`.
            TypeError: If `raw_value` type is different from `bytes` and `NoneType`.
        """
        if raw_value is None:
            self._raw_value = raw_value
            self._set_length(0)
        else:
            if not isinstance(raw_value, bytes):
                raise_type('raw_value', bytes, type(raw_value))
            self._raw_value = raw_value
            self._set_length(len(raw_value))

        try:
            self._parent._update(self)
        except AttributeError:
            pass

    @property
    def raw_length(self):
        """The encoded length field.

        Note:
            For the full data length, including the tag and length fields, use the `len` method.
        """
        return self._raw_length

    @property
    def length(self):
        """The decoded length field"""
        return self._length

    @property
    def value(self) -> Any:
        """The decoded value field"""
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        raw_value = self._encode(value)
        self._set_raw_value(raw_value)
        self._value = value
