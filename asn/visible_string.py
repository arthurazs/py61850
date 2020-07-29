from struct import pack as s_pack, unpack as s_unpack
from asn.generic_asn import GenericASN


class VisibleString(GenericASN):

    TAG = b'\x8A'

    @staticmethod
    def pack(data):
        if isinstance(data, (str, type(None), )):
            try:
                string = data.encode('utf8')
            except AttributeError:
                return VisibleString.generic_pack(None)
            # NOTE not sure if vstring is capped to 255
            # if len(string) > 255:
            #     raise ValueError('Visible string cannot be greater than 255 characters')
            return VisibleString.generic_pack(string)
        raise ValueError('Cannot pack non-string value')

    @staticmethod
    def unpack(data):
        length, string = VisibleString.generic_unpack(data)

        if length == 0:
            return None
        return string.decode('utf8')