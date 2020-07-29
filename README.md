# py61850

IEC 61850 in Python 3.

## GOOSE

You can test the generic publisher by running the following:

```bash
user@host:~/communication$ sudo python3 -m communication.goose lo
```

**NOTE**: The `lo` parameter represents the network interface which will send the GOOSE frame.  
