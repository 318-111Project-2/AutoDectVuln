CC := gcc
CFLAGS_NP = -fcf-protection=none -fno-stack-protector

make:
	$(CC) sample/src/sof1.c -o sample/sof1_32bits $(CFLAPS_NP)
	$(CC) sample/src/sof1.c -o sample/sof1_64bits $(CFLAGS_NP)
sof:
	$(CC) sample/src/sof1.c -o sample/sof1_32bits $(CFLAPS_NP)
	$(CC) sample/src/sof1.c -o sample/sof1_64bits $(CFLAGS_NP)
clean:
	rm sample/sof1_32bits sample/sof1_64bits
