/*
 	x86 (32bits) 	$ gcc -m32 sof1.c -o sof1
	x86_64 (64bits) $ gcc sof1.c -o sof1
 */
#include <stdio.h>

int main() {
	char str[10];
	
	// stack over flow
	scanf("%20s", str);
	
	printf("%s", str);
	return 0;
}
