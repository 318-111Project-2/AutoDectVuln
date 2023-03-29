/*
 	x86 (32bits) 	$ gcc -m32 no_sof1.c -o no_sof1
	x86_64 (64bits) $ gcc no_sof1.c -o no_sof1 -fcf-protection=none -fno-stack-protector

	-fcf-protection=none
		disable intel cet
	-fno-stack-protector
		disable canary
*/
#include <stdio.h>
#include <string.h>
#include <unistd.h>

void  fun1(char str[]) {
    read(0, str, 9);
}

void  fun2(char str[]) {
    read(0, str, 9);
}

int main() {
	char str[10];
	char str2[10];
	fun1(str);
	if(strcmp(str, "hi")==0){
		fun2(str2);
		printf("hi");
	}else
		printf("bye");
	return 0;
}