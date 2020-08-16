from struct import pack as s_pack
from utils.numbers import U12

GOOSE_ETHER_TYPE = b'\x88\xb8'
PRIORITIES = {  # is it useful?
    0: 'Background',
    1: 'Best effort',
    2: 'Excellent effort',
    3: 'Critical applications',
    4: 'Video, < 100 ms latency and jitter',
    5: 'Voice, < 10 ms latency and jitter',
    6: 'Internetwork control',
    7: 'Network control',
}


class VirtualLan:
    def __init__(self, ether_type=GOOSE_ETHER_TYPE, priority=4, vid=0):
        # NOTE add support for DPI == True?
        self._ether_type = ether_type
        self.priority = priority
        self.vid = vid

    def __bytes__(self):
        prio_dei = self._priority << 1  # add the DPI bit (which is always 0)
        vlan_data = (prio_dei << 12) + self._vid
        return s_pack('!H', vlan_data) + self._ether_type

    @property
    def priority(self):
        return self._priority

    @property
    def priority_desc(self):
        return PRIORITIES[self._priority]

    @priority.setter
    def priority(self, priority):
        if 0 <= priority <= 7:
            self._priority = priority
        else:
            raise ValueError('priority is out of supported range')

    @property
    def vid(self):
        return self._vid

    @vid.setter
    def vid(self, vid):
        if 0 <= vid < U12:
            self._vid = vid
        else:
            raise ValueError('vid is out of supported range')
