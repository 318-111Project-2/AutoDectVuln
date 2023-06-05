/*
	x86_64 (64bits) $ gcc sof.c -o sof -fcf-protection=none -fno-stack-protector

	-fcf-protection=none
		disable intel cet
	-fno-stack-protector
		disable canary
 */
#include <stdio.h>
#include <string.h>

void  vuln(char str[]) {
	// stack over flow
	scanf("%30s", str);
}

void  vuln2(char str[]) {
	// stack over flow
	scanf("%30s", str);
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
