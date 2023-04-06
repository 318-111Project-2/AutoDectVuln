/*
    gcc fmt.c -o fmt -fcf-protection=none -fno-stack-protector
*/
#include <stdio.h>

void vuln(char *format) {
    printf(format);
    printf("Test2");
}

int main() {
	char format[0x10];
	scanf("%s", format);
    printf("Test1");
    vuln(format);
    printf(format);
    return 0;
}