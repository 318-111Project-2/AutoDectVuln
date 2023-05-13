/*
 	gcc no_hof.c -o no_hof -fcf-protection=none -fno-stack-protector
 */
#include <stdio.h>
#include <stdlib.h>

int main() {
    unsigned long *ptr = malloc(0x50);
    *ptr = 0;
    *ptr = malloc(0x30);
    if( *ptr == NULL ) {
        fprintf(stderr, "Error: unable to allocate required memory\n");
        return 1;
    }
    read(0, *ptr, 0x30);
    write(1, *ptr, 0x30);

    free(*ptr);

    return 0;
}
