CC := gcc
CFLAGS_NP = -fcf-protection=none -fno-stack-protector

make:
	[ -d sample/build ] || mkdir -p sample/build

	$(CC) sample/src/sof1.c -o sample/build/sof1_32bits $(CFLAPS_NP)
	$(CC) sample/src/sof1.c -o sample/build/sof1_64bits $(CFLAGS_NP)
sof:
	[ -d sample/build ] || mkdir -p sample/build

	$(CC) sample/src/sof1.c -o sample/build/sof1_32bits $(CFLAPS_NP)
	$(CC) sample/src/sof1.c -o sample/build/sof1_64bits $(CFLAGS_NP)
clean:
	rm sample/build/sof1_32bits sample/build/sof1_64bits
