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
