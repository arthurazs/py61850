from iec.types.base import Base


class VisibleString(Base):

    TAG = b'\x8A'

    @staticmethod
    def pack(data, max_length=255):
        # NOTE not sure if vstring is capped to 255
        if isinstance(data, (str, type(None), )):
            # NOTE should it be null terminated?
            try:
                string = data.encode('utf8')
            except AttributeError:
                return VisibleString.generic_pack(None)
            if len(string) > max_length:
                raise ValueError(f'data cannot be greater than {max_length}')
            return VisibleString.generic_pack(string)
        raise ValueError('Cannot pack non-string value')

    @staticmethod
    def unpack(data):
        length, string = VisibleString.generic_unpack(data)

        if length == 0:
            return None
        return string.decode('utf8')
