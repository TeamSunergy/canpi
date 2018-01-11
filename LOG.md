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
