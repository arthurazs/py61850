from struct import pack as s_pack, unpack as s_unpack
from asn.utils import U7, U8, U16


class GenericASN:

    TAG = None

    @staticmethod
    def pack(data):
        raise NotImplementedError

    @staticmethod
    def unpack(data):
        raise NotImplementedError

    @classmethod
    def generic_pack(cls, packed_data):
        packed_tag = cls.TAG
        if not packed_data:
            return packed_tag + b'\x00'
        length = len(packed_data)
        if length < U7:
            packed_length = s_pack('>B', length)
        elif U7 <= length < U8:
            packed_length = s_pack(f'>BB', U7 + 1, length)
        elif U8 <= length < U16:
            packed_length = s_pack(f'>BH', U7 + 2, length)
        else:
            raise ValueError(f'GenericASN.generic_pack: packed_data length greater than {U16 - 1}')

        return packed_tag + packed_length + packed_data

    @classmethod
    def generic_unpack(cls, data):
        if data[0:1] != cls.TAG:
            raise TypeError(f'{data} is not of the {cls.TAG} type')

        try:
            length = data[1]
            extra_length = 0
            if length > U7:
                extra_length = length % U7
                if extra_length == 1:
                    length = s_unpack('>B', data[2:3])[0]
                elif extra_length == 2:
                    length = s_unpack('>H', data[2:4])[0]
                elif extra_length == 4:
                    length = s_unpack('>I', data[2:6])[0]
                elif extra_length == 8:
                    length = s_unpack('>Q', data[2:8])[0]

        except IndexError:
            raise ValueError(f'{data} is missing length field')

        value = data[2 + extra_length:]
        if length < len(value):
            raise ValueError(f'{data} seems to be incomplete')

        if length > len(value):
            raise ValueError(f'{data} seems to have extra information')

        return length, value
