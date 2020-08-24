from typing import Any, Optional, Tuple
from struct import pack as s_pack

from py61850.utils.errors import raise_type


class Base:
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

    def __bytes__(self) -> bytes:
        """Return the encoded data, including all existing fields.

        If value field is `None`: return tag + length.

        If value field is not `None`: return tag + length + value.
        """
        if self.raw_value is None:
            return self.raw_tag + self.raw_length
        return self.raw_tag + self.raw_length + self.raw_value

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

    def _parse_value(self, value: Any) -> Tuple[bytes, Any]:
        try:
            raw_value = self._encode_value(value)
            if raw_value is None:
                value = None
        except TypeError:
            raw_value = value
            value = self._decode_value(raw_value)
        return raw_value, value

    @staticmethod
    def _encode_value(value: Any) -> bytes:
        raise NotImplementedError  # pragma: no cover

    @staticmethod
    def _decode_value(value: bytes) -> Any:
        raise NotImplementedError  # pragma: no cover

    def _set_tag(self, raw_tag: bytes) -> None:
        # assert `raw_tag` is `bytes` and has length of 1, then set `raw_tag` and `tag`
        if isinstance(raw_tag, bytes):
            if len(raw_tag) == 1:
                self._raw_tag = raw_tag
                # self._tag = raw_tag.hex()
                self._tag = self.__class__.__name__
            else:
                raise ValueError('raw_tag out of supported length')
        else:
            raise_type('raw_tag', bytes, type(raw_tag))

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
            if isinstance(raw_value, bytes):
                self._raw_value = raw_value
                self._set_length(len(raw_value))
            else:
                raise_type('raw_value', bytes, type(raw_value))

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
