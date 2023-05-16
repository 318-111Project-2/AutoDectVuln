/* have 1 stack overflow */

/* spend 21s */


#include <stdio.h>
#include <string.h>

#define MAXSIZE 5

void test(char *str){
	char buf[MAXSIZE];
	strncpy(buf, str, MAXSIZE);
	printf("results: %s\n", buf); //bad
}

int main(int argc, char **argv){
	char userstr[MAXSIZE];
	scanf("%s",userstr);
	test(userstr);
	return 0;
}