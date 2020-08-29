from pytest import fixture, mark, raises

from py61850.goose.pdu import AllData, ConfigurationRevision, DataSet, GooseControlBlockReference, GooseIdentifier
from py61850.goose.pdu import GooseTimestamp, NeedsCommissioning, NumberOfDataSetEntries, SequenceNumber, StatusNumber
from py61850.goose.pdu import GooseTest, TimeAllowedToLive
from py61850.types import Boolean
from py61850.types.times import Quality


# === BOOLEAN ===
class TestNeedsCommissioning:
    @fixture
    def true(self):
        return NeedsCommissioning(True)

    @staticmethod
    def test_bytes(true):
        assert bytes(true) == b'\x89\x01\x0F'

    @staticmethod
    def test_tag(true):
        assert true.tag == 'NeedsCommissioning'


class TestGooseTest:
    @fixture
    def true(self):
        return GooseTest(True)

    @staticmethod
    def test_bytes(true):
        assert bytes(true) == b'\x87\x01\x0F'

    @staticmethod
    def test_tag(true):
        assert true.tag == 'GooseTest'


# === TIMESTAMP ===
class TestGooseTimestamp:
    @fixture
    def regular_date(self):
        return GooseTimestamp(1.1, Quality(byte=b'\x00'))

    @staticmethod
    def test_bytes(regular_date):
        assert bytes(regular_date) == b'\x84\x08\x00\x00\x00\x01\x00\x00\x01\x00'

    @staticmethod
    def test_tag(regular_date):
        assert regular_date.tag == 'GooseTimestamp'


# === UNSIGNED INTEGER ===
class TestConfigurationRevision:
    @fixture
    def zero(self):
        return ConfigurationRevision(0)

    @staticmethod
    def test_min_bytes(zero):
        assert bytes(zero) == b'\x88\x01\x00'

    @staticmethod
    def test_max_bytes():
        assert bytes(ConfigurationRevision(0xFFFFFFFF)) == b'\x88\x04\xFF\xFF\xFF\xFF'

    @staticmethod
    def test_bellow():
        assert raises(ValueError, ConfigurationRevision, -1)

    @staticmethod
    def test_above():
        assert raises(ValueError, ConfigurationRevision, 0x1FFFFFFFF)

    @staticmethod
    def test_tag(zero):
        assert zero.tag == 'ConfigurationRevision'


class TestNumberOfEntries:
    @fixture
    def zero(self):
        return NumberOfDataSetEntries(0)

    @staticmethod
    def test_min_bytes(zero):
        assert bytes(zero) == b'\x8A\x01\x00'

    @staticmethod
    def test_max_bytes():
        assert bytes(NumberOfDataSetEntries(0xFFFFFFFF)) == b'\x8A\x04\xFF\xFF\xFF\xFF'

    @staticmethod
    def test_bellow():
        assert raises(ValueError, NumberOfDataSetEntries, -1)

    @staticmethod
    def test_above():
        assert raises(ValueError, NumberOfDataSetEntries, 0x1FFFFFFFF)

    @staticmethod
    def test_tag(zero):
        assert zero.tag == 'NumberOfDataSetEntries'


class TestSequenceNumber:
    @fixture
    def zero(self):
        return SequenceNumber(0)

    @staticmethod
    def test_min_bytes(zero):
        assert bytes(zero) == b'\x86\x01\x00'

    @staticmethod
    def test_max_bytes():
        assert bytes(SequenceNumber(0xFFFFFFFF)) == b'\x86\x04\xFF\xFF\xFF\xFF'

    @staticmethod
    def test_bellow():
        assert raises(ValueError, SequenceNumber, -1)

    @staticmethod
    def test_above():
        assert raises(ValueError, SequenceNumber, 0x1FFFFFFFF)

    @staticmethod
    def test_tag(zero):
        assert zero.tag == 'SequenceNumber'


class TestStatusNumber:
    @fixture
    def one(self):
        return StatusNumber(1)

    @staticmethod
    def test_min_bytes(one):
        assert bytes(one) == b'\x85\x01\x01'

    @staticmethod
    def test_max_bytes():
        assert bytes(StatusNumber(0xFFFFFFFF)) == b'\x85\x04\xFF\xFF\xFF\xFF'

    @staticmethod
    def test_bellow():
        assert raises(ValueError, StatusNumber, -1)

    @staticmethod
    def test_above():
        assert raises(ValueError, StatusNumber, 0x1FFFFFFFF)

    @staticmethod
    def test_tag(one):
        assert one.tag == 'StatusNumber'


class TestTimeAllowedToLive:
    @fixture
    def one(self):
        return TimeAllowedToLive(1)

    @staticmethod
    def test_min_bytes(one):
        assert bytes(one) == b'\x81\x01\x01'

    @staticmethod
    def test_max_bytes():
        assert bytes(TimeAllowedToLive(0xFFFFFFFF)) == b'\x81\x04\xFF\xFF\xFF\xFF'

    @staticmethod
    def test_bellow():
        assert raises(ValueError, TimeAllowedToLive, 0)

    @staticmethod
    def test_above():
        assert raises(ValueError, TimeAllowedToLive, 0x1FFFFFFFF)

    @staticmethod
    def test_tag(one):
        assert one.tag == 'TimeAllowedToLive'


# === VISIBLE STRING ===
class TestDataSet:

    @staticmethod
    def test_bytes():
        assert bytes(DataSet('datSet')) == b'\x82\x06datSet'

    @staticmethod
    def test_bytes_none():
        assert bytes(DataSet()) == b'\x82\x00'

    @staticmethod
    def test_raw_value_none():
        assert DataSet().raw_value is None

    @staticmethod
    def test_value_none():
        assert DataSet().value is None

    @staticmethod
    def test_above():
        assert raises(ValueError, DataSet, 'a' * 66)

    @staticmethod
    def test_tag():
        assert DataSet('').tag == 'DataSet'


class TestGooseControlBlockReference:

    @staticmethod
    def test_bytes():
        assert bytes(GooseControlBlockReference('gocbRef')) == b'\x80\x07gocbRef'

    @staticmethod
    def test_bytes_none():
        assert bytes(GooseControlBlockReference()) == b'\x80\x00'

    @staticmethod
    def test_raw_value_none():
        assert GooseControlBlockReference().raw_value is None

    @staticmethod
    def test_value_none():
        assert GooseControlBlockReference().value is None

    @staticmethod
    def test_above():
        assert raises(ValueError, GooseControlBlockReference, 'a' * 66)

    @staticmethod
    def test_tag():
        assert GooseControlBlockReference('').tag == 'GooseControlBlockReference'


class TestGooseIdentifier:

    @staticmethod
    def test_bytes():
        assert bytes(GooseIdentifier('goID')) == b'\x83\x04goID'

    @staticmethod
    def test_bytes_none():
        assert bytes(GooseIdentifier()) == b'\x83\x00'

    @staticmethod
    def test_raw_value_none():
        assert GooseIdentifier().raw_value is None

    @staticmethod
    def test_value_none():
        assert GooseIdentifier().value is None

    @staticmethod
    def test_above():
        assert raises(ValueError, GooseIdentifier, 'a' * 66)

    @staticmethod
    def test_tag():
        assert GooseIdentifier('').tag == 'GooseIdentifier'


# === OTHERS ===

class TestAllData:

    DATA = {
        id: ['zero', 'one', 'two'],
        int: [0, 1, 2],
        bool: [AllData(), AllData(Boolean(False)), AllData(Boolean(False), Boolean(True))],
        bytes: [b'\xAB\x00', b'\xAB\x03\x83\x01\x00', b'\xAB\x06\x83\x01\x00\x83\x01\x0F'],
    }

    @fixture
    def none(self):
        return AllData()

    @mark.parametrize("data, byte_stream", zip(DATA[bool], DATA[bytes]), ids=DATA[id])
    def test_bytes(self, data, byte_stream):
        assert bytes(data) == byte_stream

    @mark.parametrize("data, number", zip(DATA[bool], DATA[int]), ids=DATA[id])
    def test_number_of_entries(self, data, number):
        assert data.number_of_data_set_entries == number

    @staticmethod
    def test_raw_value(none):
        assert none.raw_value is None

    @staticmethod
    def test_value(none):
        assert none.value is None

    @staticmethod
    def test_tag():
        assert AllData(Boolean(False)).tag == 'AllData'
