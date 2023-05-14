CC := gcc
CFLAGS_NP = -fcf-protection=none -fstack-protector

make:
	[ -d sample/build ] || mkdir -p sample/build

	$(CC) sample/src/simple/sof.c -o sample/build/sof $(CFLAGS_NP)
	$(CC) sample/src/simple/no_sof.c -o sample/build/no_sof $(CFLAGS_NP)
	$(CC) sample/src/simple/fmt.c -o sample/build/fmt $(CFLAPS_NP)
	$(CC) sample/src/simple/no_fmt.c -o sample/build/no_fmt $(CFLAGS_NP)
	$(CC) sample/src/simple/hof.c -o sample/build/hof $(CFLAGS_NP)
	$(CC) sample/src/simple/no_hof.c -o sample/build/no_hof $(CFLAGS_NP)
	$(CC) sample/src/simple/uaf.c -o sample/build/uaf $(CFLAGS_NP)
	$(CC) sample/src/simple/uaf2.c -o sample/build/uaf2 $(CFLAGS_NP)
	$(CC) sample/src/simple/uaf3.c -o sample/build/uaf3 $(CFLAGS_NP)
	$(CC) sample/src/simple/df.c -o sample/build/df $(CFLAGS_NP)

sof:
	[ -d sample/build ] || mkdir -p sample/build

	$(CC) sample/src/simple/sof.c -o sample/build/sof $(CFLAPS_NP)
	$(CC) sample/src/simple/no_sof.c -o sample/build/no_sof $(CFLAGS_NP)

fmt:
	[ -d sample/build ] || mkdir -p sample/build

	$(CC) sample/src/simple/fmt.c -o sample/build/fmt $(CFLAPS_NP)
	$(CC) sample/src/simple/no_fmt.c -o sample/build/no_fmt $(CFLAGS_NP)

hof:
	[ -d sample/build ] || mkdir -p sample/build

	$(CC) sample/src/simple/hof.c -o sample/build/hof $(CFLAGS_NP)
	$(CC) sample/src/simple/no_hof.c -o sample/build/no_hof $(CFLAGS_NP)

uaf:
	[ -d sample/build ] || mkdir -p sample/build

	$(CC) sample/src/simple/uaf.c -o sample/build/uaf $(CFLAGS_NP)
	$(CC) sample/src/simple/uaf2.c -o sample/build/uaf2 $(CFLAGS_NP)
	$(CC) sample/src/simple/uaf3.c -o sample/build/uaf3 $(CFLAGS_NP)

df:
	[ -d sample/build ] || mkdir -p sample/build

	$(CC) sample/src/simple/df.c -o sample/build/df $(CFLAGS_NP)
	
clean:
	rm sample/build/*
