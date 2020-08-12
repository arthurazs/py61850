from struct import pack as s_pack, unpack as s_unpack
from iec.generic_iec import GenericIEC
from iec.utils import U8, U16, U32


class UnsignedInt(GenericIEC):

    TAG = b'\x86'

    @staticmethod
    def pack(data):
        if isinstance(data, int):
            if data < 0:
                raise ValueError('Unsigned integer cannot be negative')
            elif data < U8:
                return UnsignedInt.generic_pack(s_pack('>B', data))
            elif data < U16:
                return UnsignedInt.generic_pack(s_pack('>H', data))
            # elif data < U24:
            # #     # NOTE regular MMS does not have 24 bits unsigned int
            # #     # NOTE 24 bits unsigned int seems to be used only for timestamp
            #     return UnsignedInt.generic_pack(s_pack('>I', data)[1:])
            elif data < U32:
                return UnsignedInt.generic_pack(s_pack('>I', data))
            raise ValueError('Unsigned integer out of supported range')
        raise ValueError('Cannot pack non-int value')

    @staticmethod
    def unpack(data):
        length, number = UnsignedInt.generic_unpack(data)

        if length == 0:
            return None
        elif length == 1:
            return s_unpack('>B', number)[0]
        elif length == 2:
            return s_unpack('>H', number)[0]
        # elif length == 3:
        #     # NOTE regular MMS does not have 24 bits unsigned int
        #     # NOTE 24 bits unsigned int seems to be used only for timestamp
        #     return s_unpack('>I', b'\x00' + number)[0]
        elif length == 4:
            return s_unpack('>I', number)[0]
        raise ValueError('Unsigned integer out of supported range')
