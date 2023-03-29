CC := gcc
CFLAGS_NP = -fcf-protection=none -fno-stack-protector

make:
	[ -d sample/build ] || mkdir -p sample/build

	$(CC) sample/src/sof.c -o sample/build/sof $(CFLAGS_NP)
	$(CC) sample/src/no_sof.c -o sample/build/no_sof $(CFLAGS_NP)
sof:
	[ -d sample/build ] || mkdir -p sample/build

	$(CC) sample/src/sof.c -o sample/build/sof $(CFLAPS_NP)
	$(CC) sample/src/no_sof.c -o sample/build/no_sof $(CFLAGS_NP)
clean:
	rm sample/build/sof sample/build/no_sof
