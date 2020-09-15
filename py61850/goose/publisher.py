from struct import pack as s_pack
from typing import Optional, Tuple, Union

from py61850.goose.ethernet import Ethernet
from py61850.goose.pdu import AllData, ConfigurationRevision, DataSet, GooseControlBlockReference, GooseIdentifier
from py61850.goose.pdu import GooseTimestamp, NeedsCommissioning, NumberOfDataSetEntries, ProtocolDataUnit
from py61850.goose.pdu import SequenceNumber, StatusNumber, GooseTest, TimeAllowedToLive
from py61850.goose.virtual_lan import VirtualLAN
from py61850.types.base import Base
from py61850.utils.parser import int_u16, u16_str

VLAN_ETHER_TYPE = b'\x81\x00'
GOOSE_ETHER_TYPE = b'\x88\xb8'


class Publisher:
    def __init__(self, destination: bytes = b'\x01\x0c\xcd\x01\x00\x00', source: bytes = b'\x00\x00\x00\x00\x00\x00',
                 virtual_lan: bool = True, vlan_priority: int = 4, vlan_id: int = 0, app_id: int = 1,
                 goose_control_block_reference: str = 'IED_CFG/LLN0$GO$ControlBlockReference',
                 time_allowed_to_live: int = 1000, data_set: str = 'IED_CFG/LLN0$DataSet',
                 goose_identifier: str = 'IED', goose_timestamp: float = 0.0, status_number: int = 1,
                 sequence_number: int = 0, test: bool = False, configuration_revision: int = 1,
                 needs_commissioning: bool = False, number_of_data_set_entries: Optional[int] = None,
                 all_data: Optional[Union[AllData, Tuple[Base, ...]]] = None):
        self.destination = destination
        self.source = source
        if virtual_lan:
            self._ether_type = VLAN_ETHER_TYPE
            # TODO add vlan property if, and only if, vlan set to True
            self._virtual_lan = VirtualLAN(GOOSE_ETHER_TYPE, vlan_priority, vlan_id)
        else:
            self._ether_type = GOOSE_ETHER_TYPE
            self._virtual_lan = None
        self._set_app_id(app_id)
        self._length = None  # 2 bytes
        self._reserved = b'\x00\x00\x00\x00'

        goose_control_block_reference = GooseControlBlockReference(goose_control_block_reference)
        time_allowed_to_live = TimeAllowedToLive(time_allowed_to_live)
        data_set = DataSet(data_set)
        goose_identifier = GooseIdentifier(goose_identifier)
        goose_timestamp = GooseTimestamp(goose_timestamp)
        status_number = StatusNumber(status_number)
        sequence_number = SequenceNumber(sequence_number)
        test = GooseTest(test)
        configuration_revision = ConfigurationRevision(configuration_revision)
        needs_commissioning = NeedsCommissioning(needs_commissioning)
        if number_of_data_set_entries is not None:
            number_of_data_set_entries = NumberOfDataSetEntries(number_of_data_set_entries)
        if all_data:
            if not isinstance(all_data, AllData):
                all_data = AllData(*all_data)
        else:
            all_data = AllData()

        self._pdu = ProtocolDataUnit(goose_control_block_reference, time_allowed_to_live, data_set, goose_identifier,
                                     goose_timestamp, status_number, sequence_number, test, configuration_revision,
                                     needs_commissioning, number_of_data_set_entries, all_data)

    def __bytes__(self):
        header = self._raw_destination + self._raw_source + self._ether_type
        if self._virtual_lan:
            header += bytes(self._virtual_lan)
        start = self._raw_app_id
        # TODO Implement LENGTH
        end = self._reserved + bytes(self._pdu)
        return header + start + s_pack('!H', len(start + end) + 2) + end

    def __iter__(self):
        self._iter = iter(self._pdu)
        return self

    def __next__(self):
        try:
            next(self._iter)
        except AttributeError:
            raise TypeError(f"'{self.__class__.__name__}' object is not iterable")
        return self

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

    @property
    def protocol_data_unit(self):
        return self._pdu
