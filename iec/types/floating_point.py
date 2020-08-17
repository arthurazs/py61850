from struct import pack as s_pack, unpack as s_unpack
from iec.types.base import Base


class FloatingPoint(Base):

    TAG = b'\x87'

    @staticmethod
    def pack(data, double_precision=False):
        if isinstance(data, (float, int, )):
            if double_precision:
                return FloatingPoint.generic_pack(b'\x11' + s_pack('!d', data))
            return FloatingPoint.generic_pack(b'\x08' + s_pack('!f', data))
        raise ValueError('Cannot pack non-number value')

    @staticmethod
    def _unpack_single_precision(encoded_number):
        if encoded_number[0] != 0x08:  # tag
            raise TypeError('Not a single precision floating point')
        return s_unpack('!f', encoded_number[1:5])[0]  # number

    @staticmethod
    def _unpack_double_precision(encoded_number):
        if encoded_number[0] != 0x11:  # tag
            raise TypeError('Not a double precision floating point')
        return s_unpack('!d', encoded_number[1:9])[0]  # number

    @staticmethod
    def unpack(data):
        length, encoded_number = FloatingPoint.generic_unpack(data)

        if length == 0 or length == 1:
            return None
        elif length == 5:
            return FloatingPoint._unpack_single_precision(encoded_number)
        elif length == 9:
            return FloatingPoint._unpack_double_precision(encoded_number)
        raise ValueError('Floating point out of supported range')
