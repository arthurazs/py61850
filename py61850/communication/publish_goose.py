from socket import AF_PACKET, socket, SOCK_RAW
from sys import argv
from time import time, time_ns

from py61850.goose.publisher import Publisher
from py61850.types import Boolean, VisibleString
from py61850.types.floating_point import DoublePrecision, SinglePrecision
from py61850.types.integer import Signed, Unsigned
from py61850.types.times import Quality, Timestamp

nic = socket(AF_PACKET, SOCK_RAW)
nic.bind((argv[1], 0))

now = time_ns()

data = {
    # HEADER
    'destination': b'\x01\x0c\xcd\x01\x00\x13',
    'source': b'\x7c\x8a\xe1\xd9\xcf\xbe',
    # VLAN
    'virtual_lan': True,
    'vlan_priority': 7,
    'vlan_id': 0xFFF,
    # GOOSE
    'app_id': 13,
    # PDU
    'goose_control_block_reference': 'ASD_CFG/LLN0$GO$GOOSE_SENDER',
    'time_allowed_to_live': 1000,
    'data_set': 'ASD_CFG/LLN0$MyDataSet',
    'goose_identifier': 'ASD',
    'goose_timestamp': time(),
    'status_number': 1,
    'sequence_number': 0,
    'test': True,
    'configuration_revision': 13,
    'needs_commissioning': True,
    # ALL DATA
    'all_data': (
        Boolean(True),
        VisibleString('Content'),
        DoublePrecision(1.2),
        SinglePrecision(3.4),
        Signed(-5),
        Unsigned(6),
        Timestamp(
            705762855.123456789,
            Quality(False, False, True, 13)
        )
    )
}

publisher = Publisher(**data)

goose = bytes(publisher)
nic.send(goose)

for index, goose in enumerate(publisher):
    nic.send(bytes(goose))
    if index == 0xF:
        break

print(f'{(time_ns() - now) / 1000}us')
