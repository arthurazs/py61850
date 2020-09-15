# py61850

Stable Version, Linting (PEP8) and Coverage
[![Health Status](https://github.com/arthurazs/py61850/workflows/Health (Py3.8)/badge.svg](https://github.com/arthurazs/py61850/actions?query=workflow%3A"Health+(Py3.8)")

Testing for other Python Versions 
[![Health Status](https://github.com/arthurazs/py61850/workflows/Version (Py3.6, Py3.7)/badge.svg](https://github.com/arthurazs/py61850/actions?query=workflow%3A"Version+(Py3.6,+Py3.7)")
IEC 61850 in Python 3.

## What I want it to be

### sync61850

```python
from socket import AF_PACKET, socket, SOCK_RAW
from sys import argv
from time import sleep

nic = socket(AF_PACKET, SOCK_RAW)
nic.bind((argv[1], 0))

from sansio61850.goose import Publisher
from sansio61850.types import Boolean, VisibleString
from sansio61850.types.integer import Signed, Unsigned


ied = 'IED_Pub'
ref = f'{ied}_CFG/LLN0'
data = (Boolean(True), VisibleString('Content'), Signed(-5), Unsigned(6))
publisher = Publisher(destination='01:0c:cd:01:00:13', vlan=False, app_id=1,
                      gcb_ref=f'{ref}$GO$GOOSE_SENDER', data_set=f'{ref}$MyDataSet',
                      go_id=ied, all_data=data)

for st_num, goose in enumerate(publisher):
    if st_num == 10:
        goose.pdu.all_data[1] = 'New Content'  # VisibleString
    nic.send(bytes(goose))
    sleep(goose.next_goose_timer)
```

## Roadmap

According to IEC 61850 parts 7-2, 8-1 and 9-2, and ISO 9506 parts 1 and 2. 

BER encoding.

- NEXT TODOs
 - add base.py missing test
 - move py61850 to sansio61850, sync61850
 - separate encoder from decoder

- [ ] Exceptions
  - [ ] Add custom exceptions
    - [ ] TagError
    - [ ] LengthError
    - [ ] RangeError
  - [ ] Review every exception message
  - [ ] Implement EAFP-based functions?
- [ ] Basic Types
  - [ ] Make sure data returns only the specified length, e.g.:
    - `data[1:5]` instead of `data[1:]` 
  - [ ] Care for undefined [ASN.1 length](http://luca.ntop.org/Teaching/Appunti/asn1.html)
    - `0x0000` to denote the end of the data 
  - [X] Boolean
  - [X] Unsigned Integer (ISO)
    - [ ] Enumerated (IEC)
  - [X] Signed Integer
  - [X] Floating Point
  - [X] Visible String
  - [ ] Octet String
  - [ ] MMS String (ISO) | Unicode String (IEC)
  - [X] Time Stamp
  - [ ] Time of Day (ISO) | Entry Time (IEC)  
  - [ ] Bit String (ISO) | Coded Enum (IEC)

Should py61850 support raw MMS (ISO)?

Should py61850 log what is happening? This might decrease performance.

Should support different modes of operation? (direct control, SBO, normal/enhanced sec)

Change obj.tag to return the class name instead of the hex value of raw_tag?

Should I enable changing obj value/raw_value after it being created?

Check [gridsoftware](http://www.gridsoftware.com).

Frame Generator or GOOSE Emulator? *e.g.*, Should I enable starting a GOOSE from stnum 10 instead of 0?

## Reference

- https://www.sphinx-doc.org/en/1.8/usage/extensions/example_google.html#example-google
- https://www.ossnokalva.com/asn1/resources/asn1-made-simple/introduction.html
- IEC 61850-9-2 Figure A.3 (ASN.1)

## Ideas

- Read MMS PCAP and recreate an IED
- Read GOOSE + MMS and get INFO about GOOSE
- Raspberies
- Raspberies + IEDs
- SDN
- Communication Security
- Teleprotection
- Protection
- IED Simm, simple, that sends a trip, and has gui (info tech ied sim)
- Test bed with 3 substations? to study goose cascading, etc...

## GOOSE

You can test the generic publisher by running the following:

```bash
user@host:~/communication$ sudo python3 -m communication.publish_goose lo
```

**NOTE**: The `lo` parameter represents the network interface which will send the GOOSE frame.  
