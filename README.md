# py61850

IEC 61850 in Python 3.

## Roadmap

According to IEC 61850 parts 7-2, 8-1 and 9-2, and ISO 9506 parts 1 and 2. 

- [ ] Basic Types
  - [X] Boolean
  - [X] Unsigned Integer (ISO)
    - [ ] Enumerated (IEC)
  - [X] Signed Integer
  - [ ] Floating Point
  - [X] Visible String
  - [ ] Octet String
  - [ ] MMS String (ISO) | Unicode String (IEC)
  - [ ] Time Stamp
  - [ ] Time of Day (ISO) | Entry Time (IEC)  
  - [ ] Bit String (ISO) | Coded Enum (IEC)

## GOOSE

You can test the generic publisher by running the following:

```bash
user@host:~/communication$ sudo python3 -m communication.goose lo
```

**NOTE**: The `lo` parameter represents the network interface which will send the GOOSE frame.  
