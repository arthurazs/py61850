from pytest import mark, raises

from py61850.types.times import Quality, Timestamp


class TestQuality:

    test_data = {
        id: ['min', 'max', 'generic'],
        'attr': [(False, False, False, 0), (True, True, True, 24), (False, False, True, 7)],
        bytes: [b'\x00', b'\xF8', b'\x27'],
    }

    test_error = {
        id: ['leap', 'fail', 'sync', 'acc', 'acc_range'],
        'attr': [
            ('True', True, True, 24),
            (True, 'True', True, 24),
            (True, True, 'True', 24),
            (True, True, True, '24'),
            (True, True, True, 25),
        ],
        'error': [TypeError, TypeError, TypeError, TypeError, ValueError]
    }

    @mark.parametrize("attr, byte", zip(test_data['attr'], test_data[bytes]), ids=test_data[id])
    def test_encode_attr(self, attr, byte):
        leap_second, clock_fail, clock_not_sync, accuracy = attr
        assert bytes(Quality(leap_second, clock_fail, clock_not_sync, accuracy)) == byte

    @mark.parametrize("attr, byte", zip(test_data['attr'], test_data[bytes]), ids=test_data[id])
    def test_decode_leap(self, attr, byte):
        assert Quality(raw_value=byte).leap_seconds_known == attr[0]

    @mark.parametrize("attr, byte", zip(test_data['attr'], test_data[bytes]), ids=test_data[id])
    def test_decode_fail(self, attr, byte):
        assert Quality(raw_value=byte).clock_failure == attr[1]

    @mark.parametrize("attr, byte", zip(test_data['attr'], test_data[bytes]), ids=test_data[id])
    def test_decode_sync(self, attr, byte):
        assert Quality(raw_value=byte).clock_not_synchronized == attr[2]

    @mark.parametrize("attr, byte", zip(test_data['attr'], test_data[bytes]), ids=test_data[id])
    def test_decode_accuracy(self, attr, byte):
        assert Quality(raw_value=byte).time_accuracy == attr[3]

    def test_decode_accuracy_unspecified(self):
        assert Quality(time_accuracy=0x1F).time_accuracy == 'Unspecified'

    # === EXCEPTIONS ===
    def test_decode_not_byte(self):
        assert raises(TypeError, Quality, raw_value='1')

    def test_decode_length(self):
        assert raises(ValueError, Quality, raw_value=b'')

    def test_decode_accuracy_range(self):
        assert raises(ValueError, Quality, raw_value=b'\x19')

    def test_encode_accuracy_range(self):
        assert raises(ValueError, Quality, raw_value=b'\x19')

    @mark.parametrize("attr, error", zip(test_error['attr'], test_error['error']), ids=test_error[id])
    def test_decode_attr(self, attr, error):
        leap_second, clock_fail, clock_not_sync, accuracy = attr
        assert raises(error, Quality, leap_second, clock_fail, clock_not_sync, accuracy)


class TestTimestamp:

    test_data = {
        id: ['min', 'extreme', 'generic'],
        'attr': [
            (0.0, Quality(raw_value=b'\x00')),
            (1598487698.4095, Quality(raw_value=b'\xF8')),
            (1598487698.0, Quality())],
        bytes: [
            b'\x00\x00\x00\x00\x00\x00\x00\x00',
            b'\x5F\x46\xFC\x92\x00\x0F\xFF\xF8',
            b'\x5F\x46\xFC\x92\x00\x00\x00\x20'],
    }

    @mark.parametrize("attr, byte", zip(test_data['attr'], test_data[bytes]), ids=test_data[id])
    def test_encode_attr(self, attr, byte):
        timestamp, quality = attr
        assert Timestamp(timestamp, quality).raw_value == byte

    @mark.parametrize("attr, byte", zip(test_data['attr'], test_data[bytes]), ids=test_data[id])
    def test_decode_timestamp(self, attr, byte):
        assert Timestamp(byte).value == attr[0]

    @mark.parametrize("attr, byte", zip(test_data['attr'], test_data[bytes]), ids=test_data[id])
    def test_decode_leap(self, attr, byte):
        assert Timestamp(byte).leap_seconds_known == attr[1].leap_seconds_known

    @mark.parametrize("attr, byte", zip(test_data['attr'], test_data[bytes]), ids=test_data[id])
    def test_decode_fail(self, attr, byte):
        assert Timestamp(byte).clock_failure == attr[1].clock_failure

    @mark.parametrize("attr, byte", zip(test_data['attr'], test_data[bytes]), ids=test_data[id])
    def test_decode_sync(self, attr, byte):
        assert Timestamp(byte).clock_not_synchronized == attr[1].clock_not_synchronized

    @mark.parametrize("attr, byte", zip(test_data['attr'], test_data[bytes]), ids=test_data[id])
    def test_decode_accuracy(self, attr, byte):
        assert Timestamp(byte).time_accuracy == attr[1].time_accuracy

    # === EXCEPTIONS ===
    def test_encode_type(self):
        assert raises(TypeError, Timestamp, 123)

    def test_encode_missing_quality(self):
        assert raises(TypeError, Timestamp, 123.123)

    def test_decode_length(self):
        assert raises(ValueError, Timestamp, b'')
