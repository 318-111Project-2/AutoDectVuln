CC := gcc
CFLAGS_NP = -fcf-protection=none -fstack-protector

make:
	[ -d sample/build ] || mkdir -p sample/build

	$(CC) sample/src/sof.c -o sample/build/sof $(CFLAGS_NP)
	$(CC) sample/src/no_sof.c -o sample/build/no_sof $(CFLAGS_NP)
	$(CC) sample/src/fmt.c -o sample/build/fmt $(CFLAPS_NP)
	$(CC) sample/src/no_fmt.c -o sample/build/no_fmt $(CFLAGS_NP)
	$(CC) sample/src/hof.c -o sample/build/hof $(CFLAGS_NP)
	$(CC) sample/src/no_hof.c -o sample/build/no_hof $(CFLAGS_NP)
	$(CC) sample/src/uaf.c -o sample/build/uaf $(CFLAGS_NP)
	$(CC) sample/src/uaf2.c -o sample/build/uaf2 $(CFLAGS_NP)
	$(CC) sample/src/uaf3.c -o sample/build/uaf3 $(CFLAGS_NP)
	$(CC) sample/src/df.c -o sample/build/df $(CFLAGS_NP)

sof:
	[ -d sample/build ] || mkdir -p sample/build

	$(CC) sample/src/sof.c -o sample/build/sof $(CFLAPS_NP)
	$(CC) sample/src/no_sof.c -o sample/build/no_sof $(CFLAGS_NP)

fmt:
	[ -d sample/build ] || mkdir -p sample/build

	$(CC) sample/src/fmt.c -o sample/build/fmt $(CFLAPS_NP)
	$(CC) sample/src/no_fmt.c -o sample/build/no_fmt $(CFLAGS_NP)

hof:
	[ -d sample/build ] || mkdir -p sample/build

	$(CC) sample/src/hof.c -o sample/build/hof $(CFLAGS_NP)
	$(CC) sample/src/no_hof.c -o sample/build/no_hof $(CFLAGS_NP)

uaf:
	[ -d sample/build ] || mkdir -p sample/build

	$(CC) sample/src/uaf.c -o sample/build/uaf $(CFLAGS_NP)
	$(CC) sample/src/uaf2.c -o sample/build/uaf2 $(CFLAGS_NP)
	$(CC) sample/src/uaf3.c -o sample/build/uaf3 $(CFLAGS_NP)

df:
	[ -d sample/build ] || mkdir -p sample/build

	$(CC) sample/src/df.c -o sample/build/df $(CFLAGS_NP)
	
clean:
	rm sample/build/*
