from struct import pack as s_pack, unpack as s_unpack
from asn.generic_asn import GenericASN

U8 = 255
U16 = 65535
# U24 = 16777215
U32 = 4294967295


class UnsignedInt(GenericASN):
    
    TAG = b'\x86'

    @staticmethod
    def pack(value):
        if value is None:
            return UnsignedInt.TAG + b'\x00'
        elif value < 0:
            raise ValueError('Unsigned integer cannot be negative')
        elif value <= U8:
            return UnsignedInt.TAG + b'\x01' + s_pack('>B', value)
        elif value <= U16:
            return UnsignedInt.TAG + b'\x02' + s_pack('>H', value)
        # elif value <= U24:
        # #     # NOTE regular MMS does not have 24 bits unsigned int
        # #     # NOTE 24 bits unsigned int seems to be used only for timestamp
        #     return UnsignedInt.TAG + b'\x03' + s_pack('>I', value)[1:]
        elif value <= U32:
            return UnsignedInt.TAG + b'\x04' + s_pack('>I', value)
        raise ValueError('Unsigned integer out of supported range')

    @staticmethod
    def unpack(value):
        tag, size, number = UnsignedInt.get_asn(value)

        if size == 0:
            return None
        elif size == 1:
            return s_unpack('>B', number)[0]
        elif size == 2:
            return s_unpack('>H', number)[0]
        # elif size == 3:
        #     # NOTE regular MMS does not have 24 bits unsigned int
        #     # NOTE 24 bits unsigned int seems to be used only for timestamp
        #     return s_unpack('>I', b'\x00' + number)[0]
        elif size == 4:
            return s_unpack('>I', number)[0]
        raise ValueError('Unsigned integer out of supported range')
