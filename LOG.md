# Progress Log for Send/Recv CAN messages

### Wed. 1/10/2018
Made some progress where:
- `test-send.py` sends virtual CAN (vcan) messages
- With `send.py`setup, sends 1 successful message then 2 ERR messages (check Wireshark)
- if you run `send.py`, it loops 12 times then throws OSError: (Errno 105) no buffer space available`
	- could be a Hardware issue
	- could be that we're not receiving the sent messages (could be that the buffer resets or something
		once a message has been received, so we should work on setting up `recv.py` next, on PiB

Other notes:
- did some housekeeping on both Pi devices such as removing Python2.x and keeping 3.x on both
- nuked home dir
- tmux installed on PiB
- increased font size

---

### Thurs. 1/11/2018
At this point we don't exactly know if we're sending CAN messages. Using Wireshark, we can see vcan messages.
When we try to see _can_ messages, we see 1 sent, and then typically 2 Errors. In the terminal, we see the loop runs ~12 times before throwing an OSError: no buffer space available...

If we look at the vcan test, we see that each message appears _twice_ in Wireshark; we assume this to be HI and LO signals. Looking at the CAN test message, it only sends a HI message, then the two errors. This means it's probably not sending proprerly...

Both PiA and PiB should be able to run the `test-send.py` with a vcan device setup, and `send.py` witha can device setup. 

We're looking into purchasing a OBD-II device that simply sends CAN messages, so we can know we should be getting CAN messages and focus on receiving, parsing, etc. 
