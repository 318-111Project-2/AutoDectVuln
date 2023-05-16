/* have 1 stack overflow */

/* spend 10s */

#include <stdio.h>
#include <string.h>

#define MAXSIZE 40

void test(char *str){
	char buf[MAXSIZE];
	realpath(str, buf);
	printf("results: %s\n", buf);
}

int main(int argc, char **argv){
	char userstr[MAXSIZE];
	scanf("%s",userstr);
	test(userstr);
	return 0;
}