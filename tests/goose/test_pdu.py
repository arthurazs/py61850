from pytest import fixture, raises

from py61850.goose.pdu import AllData, ConfigurationRevision, DataSet, GooseControlBlockReference, GooseIdentifier
from py61850.goose.pdu import GooseTimestamp, NeedsCommissioning, NumberOfDataSetEntries, ProtocolDataUnit
from py61850.goose.pdu import SequenceNumber, StatusNumber, GooseTest, TimeAllowedToLive
from py61850.types import Boolean


class TestProtocolDataUnit:
    @fixture
    def pdu(self):
        return ProtocolDataUnit()

    @fixture
    def cb_ref(self):
        return GooseControlBlockReference('IED_CFG/LLN0$GO$ControlBlockReference')

    @fixture
    def ttl(self):
        return TimeAllowedToLive(1000)

    @fixture
    def dat_set(self):
        return DataSet('IED_CFG/LLN0$DataSet')

    @fixture
    def go_id(self):
        return GooseIdentifier('IED')

    @fixture
    def t(self):
        return GooseTimestamp(0.0)

    @fixture
    def st_num(self):
        return StatusNumber(1)

    @fixture
    def sq_num(self):
        return SequenceNumber(0)

    @fixture
    def go_test(self):
        return GooseTest(False)

    @fixture
    def conf_rev(self):
        return ConfigurationRevision(1)

    @fixture
    def nds_com(self):
        return NeedsCommissioning(False)

    @staticmethod
    def test_bytes(pdu):
        assert bytes(pdu) == b'\x61\x64' \
                             b'\x80\x25IED_CFG/LLN0$GO$ControlBlockReference' \
                             b'\x81\x02\x03\xe8' \
                             b'\x82\x14IED_CFG/LLN0$DataSet' \
                             b'\x83\x03IED' \
                             b'\x84\x08\x00\x00\x00\x00\x00\x00\x00\x20' \
                             b'\x85\x01\x01' \
                             b'\x86\x01\x00' \
                             b'\x87\x01\x00' \
                             b'\x88\x01\x01' \
                             b'\x89\x01\x00' \
                             b'\x8a\x01\x00' \
                             b'\xab\x00'

    @staticmethod
    def test_property_cb_ref(pdu, cb_ref):
        assert bytes(pdu.goose_control_block_reference) == bytes(cb_ref)

    @staticmethod
    def test_property_ttl(pdu, ttl):
        assert bytes(pdu.time_allowed_to_live) == bytes(ttl)

    @staticmethod
    def test_property_dat_set(pdu, dat_set):
        assert bytes(pdu.data_set) == bytes(dat_set)

    @staticmethod
    def test_property_go_id(pdu, go_id):
        assert bytes(pdu.goose_identifier) == bytes(go_id)

    @staticmethod
    def test_property_t(pdu, t):
        assert bytes(pdu.goose_timestamp) == bytes(t)

    @staticmethod
    def test_property_st_num(pdu, st_num):
        assert bytes(pdu.status_number) == bytes(st_num)

    @staticmethod
    def test_property_sq_num(pdu, sq_num):
        assert bytes(pdu.sequence_number) == bytes(sq_num)

    @staticmethod
    def test_property_test(pdu, go_test):
        assert bytes(pdu.goose_test) == bytes(go_test)

    @staticmethod
    def test_property_conf_rev(pdu, conf_rev):
        assert bytes(pdu.configuration_revision) == bytes(conf_rev)

    @staticmethod
    def test_property_nds_com(pdu, nds_com):
        assert bytes(pdu.needs_commissioning) == bytes(nds_com)

    @staticmethod
    def test_wrong_num_of_entries():
        assert raises(ValueError, ProtocolDataUnit,
                      number_of_data_set_entries=NumberOfDataSetEntries(2),
                      all_data=AllData(Boolean(True)))

    @staticmethod
    def test_correct_num_of_entries():
        pdu = ProtocolDataUnit(number_of_data_set_entries=NumberOfDataSetEntries(1), all_data=AllData(Boolean(True)))
        assert pdu.number_of_data_set_entries.value == pdu.all_data.number_of_data_set_entries
