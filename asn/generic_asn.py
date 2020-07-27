
class GenericASN:

    TAG = None

    @staticmethod
    def pack(value):
        raise NotImplementedError

    @staticmethod
    def unpack(value):
        raise NotImplementedError

    @classmethod
    def get_asn(cls, value):
        tag = value[0:1]
        try:
            size = value[1]
        except IndexError:
            raise ValueError(f'{value} is missing length field')
        number = value[2:]

        if tag != cls.TAG:
            raise TypeError(f'{value} is not of the {cls.TAG} type')

        if size < len(number):
            raise ValueError(f'{value} seems to be incomplete')

        if size > len(number):
            raise ValueError(f'{value} seems to have extra information')

        return tag, size, number
