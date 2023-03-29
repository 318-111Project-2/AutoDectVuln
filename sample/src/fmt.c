/*
    gcc fmt.c -o fmt -fcf-protection=none -fno-stack-protector
*/
#include <stdio.h>

void vuln(char *format) {
    printf(format);
}

int main() {
	char format[0x10];
	scanf("%s", format);
    vuln(format);
    return 0;
}