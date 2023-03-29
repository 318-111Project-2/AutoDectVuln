/*
 	x86 (32bits) 	$ gcc -m32 sof1.c -o sof1
	x86_64 (64bits) $ gcc sof1.c -o sof1 -fcf-protection=none -fno-stack-protector

	-fcf-protection=none
		disable intel cet
	-fno-stack-protector
		disable canary
 */
#include <stdio.h>
#include <string.h>

void  vuln(char str[]) {
	// stack over flow
	scanf("%20s", str);
}

void  vuln2(char str[]) {
	// stack over flow
	scanf("%20s", str);
}

int main() {
	char str[10];
	char str2[10];
	vuln(str);
	if(strcmp(str, "hi")==0){
		vuln2(str2);
		printf("hi");
	}else
		printf("bye");
	return 0;
}
