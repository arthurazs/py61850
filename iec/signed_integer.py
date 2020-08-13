from struct import pack as s_pack, unpack as s_unpack
from iec.generic_iec import GenericIEC
from iec.utils import N8, P8, N16, P16, N32, P32, N64, P64


class SignedInt(GenericIEC):

    TAG = b'\x85'

    @staticmethod
    def pack(data):
        if isinstance(data, int):
            if N8 <= data <= P8:
                return SignedInt.generic_pack(s_pack('!b', data))
            elif N16 <= data <= P16:
                return SignedInt.generic_pack(s_pack('!h', data))
            elif N32 <= data <= P32:
                return SignedInt.generic_pack(s_pack('!i', data))
            elif N64 <= data <= P64:  # NOTE change support from 64 to 128?
                return SignedInt.generic_pack(s_pack('!q', data))
            raise ValueError('Signed integer out of supported range')
        raise ValueError('Cannot pack non-int value')

    @staticmethod
    def unpack(data):
        length, number = SignedInt.generic_unpack(data)

        if length == 0:
            return None
        elif length == 1:
            return s_unpack('!b', number)[0]
        elif length == 2:
            return s_unpack('!h', number)[0]
        elif length == 4:
            return s_unpack('!i', number)[0]
        elif length == 8:
            return s_unpack('!q', number)[0]
        raise ValueError('Signed integer out of supported range')
