# py61850

IEC 61850 in Python 3.

## Roadmap

According to IEC 61850 parts 7-2, 8-1 and 9-2, and ISO 9506 parts 1 and 2. 

BER encoding.

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
  - [X] Boolean
  - [X] Unsigned Integer (ISO)
    - [ ] Enumerated (IEC)
  - [X] Signed Integer
  - [X] Floating Point
  - [X] Visible String
  - [ ] Octet String
  - [ ] MMS String (ISO) | Unicode String (IEC)
  - [ ] Time Stamp
  - [ ] Time of Day (ISO) | Entry Time (IEC)  
  - [ ] Bit String (ISO) | Coded Enum (IEC)

Should py61850 support raw MMS (ISO)?

Should py61850 log what is happening? This might decrease performance.

## Reference

https://www.ossnokalva.com/asn1/resources/asn1-made-simple/introduction.html

## Ideas

- Read MMS PCAP and recreate an IED
- Read GOOSE + MMS and get INFO about GOOSE
- Raspberies
- Raspberies + IEDs
- SDN
- Communication Security
- Teleprotection
- Protection

## NOTE

You may convert an integer to encoded MAC address by using the `Ethernet.enet_itom()` function. Bear in mind that python supports instantiating hex values as integers, which makes it easier to convert MAC addresses, *e.g.*, `0x0123ABCD45EF`.

You may also convert strings to encoded MAC address by using the `Ethernet.enet_stom()` function. It currently supports MAC addresses with no *splitter*, *e.g.*, `0123ABCD45EF`, or with one of the following *splitter*: colon `:`; hyphen `-`; or space ` `.

```python
>>> from communication.goose.ethernet import Ethernet
>>> Ethernet.enet_itom(0)
b'\x00\x00\x00\x00\x00\x00'

>>> Ethernet.enet_itom(0x123456789abc)
b'\x12\x34\x56\x78\x9a\xbc'

>>> Ethernet.enet_stom('000000000000')
b'\x00\x00\x00\x00\x00\x00'

>>> Ethernet.enet_stom('FF-FF-FF-FF-FF-FF')
b'\xFF\xFF\xFF\xFF\xFF\xFF'
```

## GOOSE

You can test the generic publisher by running the following:

```bash
user@host:~/communication$ sudo python3 -m communication.publish_goose lo
```

**NOTE**: The `lo` parameter represents the network interface which will send the GOOSE frame.  
