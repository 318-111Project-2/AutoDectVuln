/*
 	x86 (32bits) 	$ gcc -m32 sof1.c -o sof1
	x86_64 (64bits) $ gcc sof1.c -o sof1
 */
#include <stdio.h>

void  vuln(char str[]) {
	// stack over flow
	scanf("%20s", str);
}

int main() {
	char str[10];
	vuln(str);
	printf("%s", str);
	return 0;
}
