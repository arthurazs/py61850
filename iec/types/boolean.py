from iec.types.base import Base


class Boolean(Base):

    TAG = b'\x83'

    @staticmethod
    def pack(data):
        if isinstance(data, bool):
            return Boolean.generic_pack(b'\x0F' if data else b'\x00')
        raise ValueError('Cannot pack non-boolean value')

    @staticmethod
    def unpack(data):
        length, boolean = Boolean.generic_unpack(data)

        if length == 0:
            return None
        elif length == 1:
            return False if boolean == b'\x00' else True
        raise ValueError('Boolean out of supported range')
