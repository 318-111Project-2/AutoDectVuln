CC := gcc
CFLAGS_NP = -fcf-protection=none -fno-stack-protector

make:
	$(CC) sample/stack_over_flow/src/sof1.c -o sample/stack_over_flow/sof1_32bits $(CFLAPS_NP)
	$(CC) sample/stack_over_flow/src/sof1.c -o sample/stack_over_flow/sof1_64bits $(CFLAGS_NP)
clean:
	rm sample/stack_over_flow/sof1_32bits sample/stack_over_flow/sof1_64bits
