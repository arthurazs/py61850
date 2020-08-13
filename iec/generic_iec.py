from struct import pack as s_pack, unpack as s_unpack
from iec.utils import U7, U8, U16


class GenericIEC:

    TAG = None

    @staticmethod
    def pack(data):  # pragma: no cover
        raise NotImplementedError

    @staticmethod
    def unpack(data):  # pragma: no cover
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
            packed_length = s_pack('>BB', U7 + 1, length)
        elif U8 <= length < U16:
            packed_length = s_pack('>BH', U7 + 2, length)
        else:
            raise ValueError(f'{cls.__name__}.generic_pack: packed_data length greater than {U16 - 1}')

        return packed_tag + packed_length + packed_data

    @classmethod
    def _assert_tag(cls, data):
        tag = data[0:1]
        remainder = data[1:]
        if tag != cls.TAG:
            raise TypeError(f'{tag} is not of the {cls.TAG} type')
        return tag, remainder

    @classmethod
    def _unpack_length(cls, data):
        try:
            length = data[0]
        except IndexError:
            raise ValueError(f'{data} is missing length field')

        extra_length = 0
        if length > U7:
            extra_length = length % U7
            if extra_length == 1:
                length = s_unpack('>B', data[1:2])[0]
            elif extra_length == 2:
                length = s_unpack('>H', data[1:3])[0]
            elif extra_length == 4:
                length = s_unpack('>I', data[1:5])[0]
            elif extra_length == 8:  # pragma: no cover
                # not worth to test (cpu intensive)
                length = s_unpack('>Q', data[1:9])[0]
            else:
                raise NotImplementedError('TODO')

        return length, extra_length, data[extra_length + 1:]

    @classmethod
    def generic_unpack(cls, data):
        _, data = cls._assert_tag(data)

        length, _, value = cls._unpack_length(data)

        if length < len(value):
            raise ValueError(f'{data} seems to be incomplete')

        if length > len(value):
            raise ValueError(f'{data} seems to have extra information')

        return length, value
