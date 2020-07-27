from struct import pack as s_pack, unpack as s_unpack
from asn.generic_asn import GenericASN

N8, P8 = -128, 127
N16, P16 = -32768, 32767
N32, P32 = -2147483648, 2147483647
N64, P64 = -9223372036854775808, 9223372036854775807


class SignedInt(GenericASN):
    
    TAG = b'\x85'

    @staticmethod
    def pack(value):
        if value is None:
            return SignedInt.TAG + b'\x00'
        elif N8 <= value <= P8:
            return SignedInt.TAG + b'\x01' + s_pack('>b', value)
        elif N16 <= value <= P16:
            return SignedInt.TAG + b'\x02' + s_pack('>h', value)
        elif N32 <= value <= P32:
            return SignedInt.TAG + b'\x04' + s_pack('>i', value)
        elif N64 <= value <= P64:
            return SignedInt.TAG + b'\x08' + s_pack('>q', value)
        raise ValueError('Signed integer out of supported range')

    @staticmethod
    def unpack(value):
        tag, size, number = SignedInt.get_asn(value)

        if size == 0:
            return None
        elif size == 1:
            return s_unpack('>b', number)[0]
        elif size == 2:
            return s_unpack('>h', number)[0]
        elif size == 4:
            return s_unpack('>i', number)[0]
        elif size == 8:
            return s_unpack('>q', number)[0]
        raise ValueError('Signed integer out of supported range')
