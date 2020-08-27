from struct import pack as s_pack, Struct
from py61850.utils.numbers import U48
from py61850.utils.errors import raise_type


class Ethernet:

    @staticmethod
    def enet_itoe(integer, max_range=0xFFFF):
        # integer to ether type
        if isinstance(integer, int):
            if 0 <= integer <= max_range:
                return s_pack('!H', integer)
            raise ValueError('integer out of supported range')
        raise_type('integer', int, type(integer))

    @staticmethod
    def enet_stoe(string):
        # string to ether type
        if isinstance(string, str):
            if len(string) == 4:
                return s_pack('!H', int(string, 16))
            raise ValueError('string out of supported length')
        raise_type('string', str, type(string))

    @staticmethod
    def pack_ether_type(ether_type):
        if isinstance(ether_type, bytes):
            return ether_type
        elif isinstance(ether_type, int):
            return Ethernet.enet_itoe(ether_type)
        elif isinstance(ether_type, str):
            return Ethernet.enet_stoe(ether_type)
        raise_type('ether_type', (bytes, int, str), type(ether_type))

    @staticmethod
    def unpack_ether_type(byte_stream):
        # ether type to string
        if isinstance(byte_stream, bytes):
            if len(byte_stream) == 2:
                return byte_stream.hex().upper()
            raise ValueError('byte_stream out of supported range')
        raise_type('byte_stream', bytes, type(byte_stream))

    @staticmethod
    def enet_etos(byte_stream):
        return Ethernet.unpack_ether_type(byte_stream)

    @staticmethod
    def assert_destination(byte_stream):
        # according to IEC 61850-8-1
        if isinstance(byte_stream, bytes):
            if len(byte_stream) == 6:
                if byte_stream[0:4] == b'\x01\x0c\xcd\x01':
                    if 0 <= byte_stream[4] <= 1:
                        return True
                    raise ValueError('fifth octet out of supported range')
                raise ValueError('first four octets do not represent a GOOSE multicast address')
            raise ValueError('byte_stream out of supported range')
        raise_type('byte_stream', bytes, type(byte_stream))

    @staticmethod
    def pack_mac_address(mac_address):
        if isinstance(mac_address, bytes):
            return mac_address
        elif isinstance(mac_address, int):
            return Ethernet.enet_itom(mac_address)
        elif isinstance(mac_address, str):
            return Ethernet.enet_stom(mac_address)
        raise_type('mac_address', (bytes, int, str), type(mac_address))

    @staticmethod
    def unpack_mac_address(byte_stream, splitter='-'):
        if isinstance(byte_stream, bytes):
            if len(byte_stream) == 6:
                address = byte_stream.hex()
                return splitter.join(address[index:index + 2] for index in range(0, len(address), 2)).upper()
            raise ValueError('byte_stream out of supported range')
        raise_type('byte_stream', bytes, type(byte_stream))

    @staticmethod
    def enet_mtos(byte_stream):
        # mac to string
        return Ethernet.unpack_mac_address(byte_stream)

    @staticmethod
    def enet_itom(integer):
        # integer to mac
        if isinstance(integer, int):
            if 0 <= integer < U48:
                return s_pack('!Q', integer)[2:]
            raise ValueError('integer out of supported range')
        raise_type('integer', int, type(integer))

    @staticmethod
    def enet_stom(string):
        # string to mac
        # NOTE Should enet_aton be smarter? e.g. accept 0::0?
        if isinstance(string, str):
            if len(string) == 17:
                # TODO Improve this function, it should accept any type of 'splitter'
                for splitter in [':', '-', ' ']:
                    if splitter in string:
                        unsigned_char = Struct('!B')
                        mac_address = b''
                        for byte in string.split(splitter):
                            mac_address += unsigned_char.pack(int(byte, 16))
                        return mac_address
                else:
                    # TODO Improve 'malformed' checking
                    raise ValueError('string seems to be malformed')
            elif len(string) == 12:
                return Ethernet.enet_itom(int(string, 16))
            raise ValueError('string out of supported range')
        raise_type('string', str, type(string))
