all:
	gcc -Isrc -fPIC $(pkg-config --cflags --libs python3) -c interpret_CAN.c interpret_CAN_wrap.c
	gcc -shared -fPIC -o interpret_CAN.so interpret_CAN.o interpret_CAN_wrap.o
	cp interpret_CAN.so ../sim/
