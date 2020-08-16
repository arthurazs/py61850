# py61850

IEC 61850 in Python 3.

## Roadmap

According to IEC 61850 parts 7-2, 8-1 and 9-2, and ISO 9506 parts 1 and 2. 

- [ ] Exceptions
  - [ ] Add custom exceptions
    - [ ] TagError
    - [ ] LengthError
    - [ ] RangeError
  - [ ] Review every exception message
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

## GOOSE

You can test the generic publisher by running the following:

```bash
user@host:~/communication$ sudo python3 -m communication.publish_goose lo
```

**NOTE**: The `lo` parameter represents the network interface which will send the GOOSE frame.  
