from py61850.goose.ethernet import Ethernet
from py61850.goose.virtual_lan import VirtualLAN
from py61850.utils.parser import int_u16, u16_str

VLAN_ETHER_TYPE = b'\x81\x00'
GOOSE_ETHER_TYPE = b'\x88\xb8'


class Publisher:
    def __init__(self, destination=b'\x01\x0c\xcd\x01\x00\x00', source=b'\x00\x00\x00\x00\x00\x00',
                 virtual_lan=True, vlan_priority=4, vlan_id=0, app_id=1):
        self.destination = destination
        self.source = source
        if virtual_lan:
            self._ether_type = VLAN_ETHER_TYPE
            # TODO add vlan property if, and only if, vlan set to True
            self._virtual_lan = VirtualLAN(GOOSE_ETHER_TYPE, vlan_priority, vlan_id)
        else:
            self._ether_type = GOOSE_ETHER_TYPE
        self._set_app_id(app_id)
        self._length = None  # 2 bytes
        self._reserved = b'\x00\x00\x00\x00'

    @property
    def raw_destination(self):
        return self._raw_destination

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, mac_address):
        self._raw_destination = Ethernet.pack_mac_address(mac_address)
        Ethernet.assert_destination(self._raw_destination)
        if isinstance(mac_address, str):
            self._destination = mac_address.upper()
        else:
            self._destination = Ethernet.unpack_mac_address(mac_address)

    @property
    def raw_source(self):
        return self._raw_source

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, mac_address):
        self._raw_source = Ethernet.pack_mac_address(mac_address)
        if isinstance(mac_address, str):
            self._source = mac_address.upper()
        else:
            self._source = Ethernet.unpack_mac_address(mac_address)

    @property
    def raw_app_id(self):
        return self._raw_app_id

    @property
    def app_id(self):
        return self._app_id

    def _set_app_id(self, app_id: int):
        self._raw_app_id = int_u16(app_id)
        self._app_id = u16_str(self._raw_app_id)
