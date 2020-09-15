from typing import NoReturn, Optional, Tuple

from py61850.types import Boolean, VisibleString
from py61850.types.base import Base
from py61850.types.integer import Unsigned
from py61850.types.times import Quality, Timestamp
from py61850.utils.errors import raise_type


class GooseControlBlockReference(VisibleString):
    def __init__(self, string: str = None):
        super().__init__(string, max_length=65, raw_tag=b'\x80')


class TimeAllowedToLive(Unsigned):
    def __init__(self, integer: int):
        # TODO Follow goose sending rate (should decrease with a new event/status number)
        # Should it though?
        super().__init__(integer, min_range=1, max_range=0xFFFFFFFF, raw_tag=b'\x81')

    @property
    def tag(self) -> str:
        """The class name."""
        return self.__class__.__name__


class DataSet(VisibleString):
    def __init__(self, string: str = None):
        super().__init__(string, max_length=65, raw_tag=b'\x82')


class GooseIdentifier(VisibleString):
    def __init__(self, string: str = None):
        super().__init__(string, max_length=65, raw_tag=b'\x83')


class GooseTimestamp(Timestamp):
    def __init__(self, epoch: float, quality: Quality = Quality()):
        super().__init__(epoch, quality, raw_tag=b'\x84')


class StatusNumber(Unsigned):
    def __init__(self, integer: int):
        super().__init__(integer, min_range=1, max_range=0xFFFFFFFF, raw_tag=b'\x85')
        self._iter = False

    def __iter__(self):
        # TODO Return a different object? #asd
        # next(obj) should not affect the original object
        self._iter = True
        return self

    def __next__(self):
        try:
            if self._iter:
                self.value += 1
                return self
            else:
                raise TypeError(f"'{self.__class__.__name__}' object is not iterable")
        except ValueError:
            self._iter = False
            raise StopIteration

    @property
    def tag(self) -> str:
        """The class name."""
        return self.__class__.__name__


class SequenceNumber(Unsigned):
    def __init__(self, integer: int):
        super().__init__(integer, min_range=0, max_range=0xFFFFFFFF, raw_tag=b'\x86')

    def __iter__(self):
        self._first = True
        return self

    def __next__(self):
        try:
            if self._first is False:
                self.value += 1
            self._first = False
            return self
        except ValueError:
            raise StopIteration
        except AttributeError:
            raise TypeError(f"'{self.__class__.__name__}' object is not iterable")

    @property
    def tag(self) -> str:
        """The class name."""
        return self.__class__.__name__


class GooseTest(Boolean):
    def __init__(self, boolean: bool):
        super().__init__(boolean, raw_tag=b'\x87')


class ConfigurationRevision(Unsigned):
    def __init__(self, integer: int):
        super().__init__(integer, min_range=0, max_range=0xFFFFFFFF, raw_tag=b'\x88')

    @property
    def tag(self) -> str:
        """The class name."""
        return self.__class__.__name__


class NeedsCommissioning(Boolean):
    def __init__(self, boolean: bool):
        super().__init__(boolean, raw_tag=b'\x89')


class NumberOfDataSetEntries(Unsigned):
    def __init__(self, integer: int):
        # TODO whats the limit?
        super().__init__(integer, min_range=0, max_range=0xFFFFFFFF, raw_tag=b'\x8A')

    @property
    def tag(self) -> str:
        """The class name."""
        return self.__class__.__name__


class AllData(Base):
    def __init__(self, *data: Base):
        # TODO Take into account 1500 (Payload limit) - GOOSE Overhead
        (raw_value, number_of_entries), value = self._parse(data)
        if raw_value == b'':
            raw_value, value = None, None
        self._value = value
        super().__init__(raw_tag=b'\xAB', raw_value=raw_value)
        self._number_of_entries = number_of_entries
        try:
            for value in self._value:
                value.set_parent(self)
        except TypeError:
            pass

    @staticmethod
    def _encode(value: Tuple[Base, ...]) -> Tuple[bytes, int]:
        # TODO Improve
        # if value is None: return None, 0

        all_data = b''
        for base in value:
            # TODO validate against standard types instead of Base?
            # like, test if v_str, u_int, s_int, f_32, f_64, etc
            # like, raise error for g_t_smp, sq_num, etc
            if not isinstance(base, Base):
                raise_type('base', Base, type(base))
            all_data += bytes(base)
        return all_data, len(value)

    @staticmethod
    def _decode(raw_value: bytes) -> NoReturn:
        # TODO Implement
        raise NotImplementedError

    @property
    def number_of_data_set_entries(self):
        return self._number_of_entries

    def __getitem__(self, item):
        return self._value[item]


class ProtocolDataUnit(Base):
    _DATA_TYPES = [('control_block_reference', GooseControlBlockReference), ('time_allowed_to_live', TimeAllowedToLive),
                   ('data_set', DataSet), ('goose_identifier', GooseIdentifier), ('goose_timestamp', GooseTimestamp),
                   ('status_number', StatusNumber), ('sequence_number', SequenceNumber), ('test', GooseTest),
                   ('configuration_revision', ConfigurationRevision), ('needs_commissioning', NeedsCommissioning),
                   ('skip', None), ('all_data', AllData)]

    # Table 56 (61850-8-1)
    def __init__(self,
                 control_block_reference: GooseControlBlockReference, time_allowed_to_live: TimeAllowedToLive,
                 data_set: DataSet, goose_identifier: GooseIdentifier, goose_timestamp: GooseTimestamp,
                 status_number: StatusNumber, sequence_number: SequenceNumber, test: GooseTest,
                 configuration_revision: ConfigurationRevision, needs_commissioning: NeedsCommissioning,
                 # TODO remove numOfDatSet from here, remove default value for AllData
                 number_of_data_set_entries: Optional[NumberOfDataSetEntries] = None, all_data: AllData = AllData(),
                 raw_value: bytes = None):
        # TODO What if the user want's to exclude some unnecessary fields
        # e.g. remove nds_com and test fields
        if raw_value:
            raise NotImplementedError
        else:
            raw_value, number_of_data_set_entries = self._encode((control_block_reference, time_allowed_to_live,
                                                                  data_set, goose_identifier, goose_timestamp,
                                                                  status_number, sequence_number, test,
                                                                  configuration_revision, needs_commissioning,
                                                                  number_of_data_set_entries, all_data))
        super().__init__(raw_tag=b'\x61', raw_value=raw_value)
        self._value = (control_block_reference, time_allowed_to_live, data_set, goose_identifier, goose_timestamp,
                       status_number, sequence_number, test, configuration_revision, needs_commissioning,
                       number_of_data_set_entries, all_data)
        for value in self._value:
            value.set_parent(self)

    def __iter__(self):
        self._iter = True
        self._iter_status = iter(self.status_number)
        self._iter_sequence = iter(self.sequence_number)
        return self

    def __next__(self):
        try:
            # update time allowed to live + time stamp
            self._iter
            next(self._iter_sequence)
        except StopIteration:
            self.sequence_number.value = 1
            self._iter_sequence = iter(self.sequence_number)
            next(self._iter_sequence)
        except AttributeError:
            raise TypeError(f"'{self.__class__.__name__}' object is not iterable")
        self._generic_update()
        return self

    def _generic_update(self):
        byte_stream = b''
        for value in self._value:
            byte_stream += bytes(value)
        self._set_raw_value(byte_stream)

    def _update(self, caller: Base):
        if isinstance(caller, AllData):
            # TODO what if i change a value for the same value? Should update trigger?
            try:
                # TODO only change if next was already called
                # e.g. pdu.all_data[0] = 1; pdu.all_data[1] = 'Okay' \
                # should generate only ONE new status change, not 2
                self._iter
                next(self._iter_status)
                self.sequence_number.value = 0
                self._iter_sequence = iter(self.sequence_number)
            except AttributeError:
                pass
            self._generic_update()

    @staticmethod
    def _assert_type(data):
        for value, data_type in zip(data, ProtocolDataUnit._DATA_TYPES):
            name, type_class = data_type
            if name == 'skip':
                continue
            if not isinstance(value, type_class):
                # TODO Test
                raise_type(name, type_class, type(value))

    @staticmethod
    def _encode(value: Tuple[GooseControlBlockReference, TimeAllowedToLive, DataSet, GooseIdentifier, GooseTimestamp,
                             StatusNumber, SequenceNumber, GooseTest, ConfigurationRevision, NeedsCommissioning,
                             NumberOfDataSetEntries, AllData]) -> Tuple[bytes, NumberOfDataSetEntries]:

        ProtocolDataUnit._assert_type(value)

        (control_block_reference, time_allowed_to_live, data_set, goose_identifier, goose_timestamp,
         status_number, sequence_number, test, configuration_revision, needs_commissioning,
         number_of_data_set_entries, all_data) = value

        if number_of_data_set_entries is None:
            number_of_data_set_entries = NumberOfDataSetEntries(all_data.number_of_data_set_entries)
        elif not isinstance(number_of_data_set_entries, NumberOfDataSetEntries):
            raise_type('number_of_data_set_entries', NumberOfDataSetEntries, type(number_of_data_set_entries))

        if number_of_data_set_entries.value != all_data.number_of_data_set_entries:
            raise ValueError('number_of_data_set_entries doest not match all_data number of entries')

        return \
            bytes(control_block_reference) + bytes(time_allowed_to_live) + bytes(data_set) + \
            bytes(goose_identifier) + bytes(goose_timestamp) + bytes(status_number) + bytes(sequence_number) + \
            bytes(test) + bytes(configuration_revision) + bytes(needs_commissioning) + \
            bytes(number_of_data_set_entries) + bytes(all_data), number_of_data_set_entries

    @staticmethod
    def _decode(raw_value: bytes) -> NoReturn:
        # TODO Implement
        raise NotImplementedError

    @property
    def goose_control_block_reference(self):
        return self._value[0]

    @property
    def time_allowed_to_live(self):
        return self._value[1]

    @property
    def data_set(self):
        return self._value[2]

    @property
    def goose_identifier(self):
        return self._value[3]

    @property
    def goose_timestamp(self):
        return self._value[4]

    @property
    def status_number(self):
        return self._value[5]

    @property
    def sequence_number(self):
        return self._value[6]

    @property
    def goose_test(self):
        return self._value[7]

    @property
    def configuration_revision(self):
        return self._value[8]

    @property
    def needs_commissioning(self):
        return self._value[9]

    @property
    def number_of_data_set_entries(self):
        return self._value[10]

    @property
    def all_data(self):
        return self._value[11]
