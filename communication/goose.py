from socket import socket, AF_PACKET, SOCK_RAW
from sys import argv
from struct import pack
from asn.visible_string import VisibleString
from asn.boolean import Boolean
from asn.signed_integer import SignedInt


def pack_data(tag, data):
    return tag + pack('>B', len(data)) + data


goose = socket(AF_PACKET, SOCK_RAW)
goose.bind((argv[1], 0))

destination = b'\x01\x0c\xcd\x01\x00\x03'
source = b'\x2c\x4d\x54\x4b\x0d\x56'
ether_type = b'\x81\x00'  # vLAN

v_lan = b'\x80\x03\x88\xb8'

time_atl = b'\x81\x02' + pack('>H', 1000)

go_cb_ref = pack_data(b'\x80', b'GE_GOOSECFG/LLN0$GO$TapsTransformador')
dat_set = pack_data(b'\x82', b'GE_GOOSECFG/LLN0$TapsTransformador')
go_id = pack_data(b'\x83', b'GE_GOOSE')

time_stamp = pack_data(
    tag=b'\x84',
    data=b'\x5f\x0f\x5c\xd7\xf4\xf7\x65\xbf'
)
st_num = b'\x85\x01' + pack('>B', 1)
sq_num = b'\x86\x01' + pack('>B', 1)
test_bit = b'\x87\x01\x00'
conf_rev = b'\x88\x01' + pack('>B', 1)
nds_com = b'\x89\x01\x00'

entries = [VisibleString.pack('Arthur'), Boolean.pack(True), SignedInt.pack(13)]
dat_set_entries = b'\x8a\x01' + pack('>B', len(entries))
booleans = b''.join(entries)
all_data = b'\xab' + pack('>B', len(booleans)) + booleans

reserved = b'\x00\x00\x00\x00'
pdu = go_cb_ref + time_atl + dat_set + go_id + time_stamp + st_num + sq_num + \
      test_bit + conf_rev + nds_com + dat_set_entries + all_data

# assert len(pdu) < 128
pdu_info = b'\x61\x81' + pack('>B', len(pdu)) + pdu
goose_frame = reserved + pdu_info

app_id = b'\x00\x03'
goose_frame = app_id + pack('>H', len(goose_frame) + 4) + goose_frame
goose.send(
    destination + source + ether_type +
    v_lan + goose_frame
)
