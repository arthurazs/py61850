from pytest import fixture, raises

from py61850.goose.pdu import AllData, ConfigurationRevision, DataSet, GooseControlBlockReference, GooseIdentifier
from py61850.goose.pdu import GooseTimestamp, NeedsCommissioning, NumberOfDataSetEntries, ProtocolDataUnit
from py61850.goose.pdu import SequenceNumber, StatusNumber, GooseTest, TimeAllowedToLive
from py61850.types import Boolean, VisibleString


class TestProtocolDataUnit:

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

    @fixture
    def num_entries(self):
        return NumberOfDataSetEntries(1)

    @fixture
    def all_data(self):
        return AllData(Boolean(True))

    @fixture
    def pdu(self, cb_ref, ttl, dat_set, go_id, t, st_num, sq_num, go_test, conf_rev, nds_com):
        return ProtocolDataUnit(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num, go_test, conf_rev, nds_com)

    @fixture
    def iter_pdu(self, pdu):
        return iter(pdu)

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
    def test_wrong_num_of_entries(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                                  go_test, conf_rev, nds_com, all_data):
        with raises(ValueError):
            ProtocolDataUnit(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num, go_test,
                             conf_rev, nds_com, NumberOfDataSetEntries(2), all_data)

    @staticmethod
    def test_correct_num_of_entries(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                                    go_test, conf_rev, nds_com, num_entries, all_data):
        pdu = ProtocolDataUnit(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                               go_test, conf_rev, nds_com, num_entries, all_data)
        assert pdu.number_of_data_set_entries.value == pdu.all_data.number_of_data_set_entries

    @staticmethod
    def test_error_cb_ref(ttl, dat_set, go_id, t, st_num, sq_num, go_test, conf_rev, nds_com, num_entries, all_data):
        with raises(TypeError):
            ProtocolDataUnit(1, dat_set, go_id, t, st_num, sq_num,
                             go_test, conf_rev, nds_com, num_entries, all_data)

    @staticmethod
    def test_error_ttl(cb_ref, dat_set, go_id, t, st_num, sq_num, go_test, conf_rev, nds_com, num_entries, all_data):
        with raises(TypeError):
            ProtocolDataUnit(cb_ref, 1, dat_set, go_id, t, st_num, sq_num,
                             go_test, conf_rev, nds_com, num_entries, all_data)

    @staticmethod
    def test_error_dat_set(cb_ref, ttl, go_id, t, st_num, sq_num, go_test, conf_rev, nds_com, num_entries, all_data):
        with raises(TypeError):
            ProtocolDataUnit(cb_ref, ttl, 1, go_id, t, st_num, sq_num,
                             go_test, conf_rev, nds_com, num_entries, all_data)

    @staticmethod
    def test_error_go_id(cb_ref, ttl, dat_set, t, st_num, sq_num, go_test, conf_rev, nds_com, num_entries, all_data):
        with raises(TypeError):
            ProtocolDataUnit(cb_ref, ttl, dat_set, 1, t, st_num, sq_num,
                             go_test, conf_rev, nds_com, num_entries, all_data)

    @staticmethod
    def test_error_t(cb_ref, ttl, dat_set, go_id, st_num, sq_num, go_test, conf_rev, nds_com, num_entries, all_data):
        with raises(TypeError):
            ProtocolDataUnit(cb_ref, ttl, dat_set, go_id, 1, st_num, sq_num,
                             go_test, conf_rev, nds_com, num_entries, all_data)

    @staticmethod
    def test_error_st_num(cb_ref, ttl, dat_set, go_id, t, sq_num, go_test, conf_rev, nds_com, num_entries, all_data):
        with raises(TypeError):
            ProtocolDataUnit(cb_ref, ttl, dat_set, go_id, t, 1, sq_num,
                             go_test, conf_rev, nds_com, num_entries, all_data)

    @staticmethod
    def test_error_sq_num(cb_ref, ttl, dat_set, go_id, t, st_num, go_test, conf_rev, nds_com, num_entries, all_data):
        with raises(TypeError):
            ProtocolDataUnit(cb_ref, ttl, dat_set, go_id, t, st_num, 1,
                             go_test, conf_rev, nds_com, num_entries, all_data)

    @staticmethod
    def test_error_go_test(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num, conf_rev, nds_com, num_entries, all_data):
        with raises(TypeError):
            ProtocolDataUnit(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                             1, conf_rev, nds_com, num_entries, all_data)

    @staticmethod
    def test_error_conf_rev(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num, go_test, nds_com, num_entries, all_data):
        with raises(TypeError):
            ProtocolDataUnit(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                             go_test, 1, nds_com, num_entries, all_data)

    @staticmethod
    def test_error_nds_com(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num, go_test, conf_rev, num_entries, all_data):
        with raises(TypeError):
            ProtocolDataUnit(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                             go_test, conf_rev, 1, num_entries, all_data)

    @staticmethod
    def test_error_num_entries(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num, go_test, conf_rev, nds_com, all_data):
        with raises(TypeError):
            ProtocolDataUnit(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                             go_test, conf_rev, nds_com, 1, all_data)

    @staticmethod
    def test_error_all_data(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num, go_test, conf_rev, nds_com, num_entries):
        with raises(TypeError):
            ProtocolDataUnit(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                             go_test, conf_rev, nds_com, num_entries, 1)

    @staticmethod
    def test_no_iter(pdu):
        with raises(TypeError) as info:
            next(pdu)
        assert str(info.value) == "'ProtocolDataUnit' object is not iterable"

    @staticmethod
    def test_iter_first_st(iter_pdu):
        assert next(iter_pdu).status_number.value == 1

    @staticmethod
    def test_iter_first_sq(iter_pdu):
        assert next(iter_pdu).sequence_number.value == 0

    @staticmethod
    def test_iter_second_st(iter_pdu):
        next(iter_pdu)
        assert next(iter_pdu).status_number.value == 1

    @staticmethod
    def test_iter_second_sq(iter_pdu):
        next(iter_pdu)
        assert next(iter_pdu).sequence_number.value == 1

    @staticmethod
    def test_iter_last_st(pdu):
        pdu.sequence_number.value = 0xFFFFFFFF
        iter_pdu = iter(pdu)
        next(iter_pdu)
        assert next(iter_pdu).status_number.value == 1

    @staticmethod
    def test_iter_last_sq(pdu):
        pdu.sequence_number.value = 0xFFFFFFFF
        iter_pdu = iter(pdu)
        next(iter_pdu)
        assert next(iter_pdu).sequence_number.value == 1

    @staticmethod
    def test_all_data_change_no_iter_st(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                                        go_test, conf_rev, nds_com, num_entries, all_data):
        pdu = ProtocolDataUnit(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                               go_test, conf_rev, nds_com, num_entries, all_data)
        pdu.all_data[0].value = False
        assert pdu.status_number.value == 1

    @staticmethod
    def test_all_data_change_no_iter_sq(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                                        go_test, conf_rev, nds_com, num_entries, all_data):
        pdu = ProtocolDataUnit(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                               go_test, conf_rev, nds_com, num_entries, all_data)
        pdu.all_data[0].value = False
        assert pdu.sequence_number.value == 0

    @staticmethod
    def test_all_data_change_iter_st(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                                     go_test, conf_rev, nds_com, num_entries, all_data):
        pdu = ProtocolDataUnit(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                               go_test, conf_rev, nds_com, num_entries, all_data)
        iter_pdu = iter(pdu)
        iter_pdu.all_data[0].value = False
        assert pdu.status_number.value == 2

    @staticmethod
    def test_all_data_change_iter_sq(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                                     go_test, conf_rev, nds_com, num_entries, all_data):
        pdu = ProtocolDataUnit(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                               go_test, conf_rev, nds_com, num_entries, all_data)
        iter_pdu = iter(pdu)
        iter_pdu.all_data[0].value = False
        assert pdu.sequence_number.value == 0

    @staticmethod
    def test_all_data_change_no_iter_error(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                                           go_test, conf_rev, nds_com, num_entries, all_data):
        pdu = ProtocolDataUnit(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                               go_test, conf_rev, nds_com, num_entries, all_data)
        with raises(TypeError) as info:
            next(pdu)
        assert str(info.value) == "'ProtocolDataUnit' object is not iterable"

    @staticmethod
    def test_all_data_change_next_st(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                                     go_test, conf_rev, nds_com, num_entries, all_data):
        pdu = ProtocolDataUnit(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                               go_test, conf_rev, nds_com, num_entries, all_data)
        iter_pdu = iter(pdu)
        iter_pdu.all_data[0].value = False
        assert next(pdu).status_number.value == 2

    @staticmethod
    def test_all_data_change_next_sq(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                                     go_test, conf_rev, nds_com, num_entries, all_data):
        pdu = ProtocolDataUnit(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                               go_test, conf_rev, nds_com, num_entries, all_data)
        iter_pdu = iter(pdu)
        iter_pdu.all_data[0].value = False
        assert next(pdu).sequence_number.value == 0

    @staticmethod
    def test_all_data_change_next_2_st(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                                       go_test, conf_rev, nds_com, num_entries, all_data):
        pdu = ProtocolDataUnit(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                               go_test, conf_rev, nds_com, num_entries, all_data)
        iter_pdu = iter(pdu)
        iter_pdu.all_data[0].value = False
        next(iter_pdu)
        assert next(pdu).status_number.value == 2

    @staticmethod
    def test_all_data_change_next_2_sq(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                                       go_test, conf_rev, nds_com, num_entries, all_data):
        pdu = ProtocolDataUnit(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num,
                               go_test, conf_rev, nds_com, num_entries, all_data)
        iter_pdu = iter(pdu)
        iter_pdu.all_data[0].value = False
        next(iter_pdu)
        assert next(pdu).sequence_number.value == 1

    @staticmethod
    def test_pdu_above(cb_ref, ttl, dat_set, go_id, t, st_num, sq_num, go_test, conf_rev, nds_com):
        with raises(ValueError) as info:
            all_data = (VisibleString('a' * 255), VisibleString('a' * 255),
                        VisibleString('a' * 255), VisibleString('a' * 255),
                        VisibleString('a' * 255), VisibleString('a' * 99))
            ProtocolDataUnit(cb_ref, ttl, dat_set, go_id, t,
                             st_num, sq_num, go_test, conf_rev, nds_com,
                             None, AllData(*all_data))
        assert str(info.value) == "ProtocolDataUnit out of supported length"
