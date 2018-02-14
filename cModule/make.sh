all:
	gcc -Isrc -fPIC $(pkg-config --cflags --libs python3) -c testc.c testc_wrap.c
	gcc -shared -fPIC -o testc.so testc.o testc_wrap.o
