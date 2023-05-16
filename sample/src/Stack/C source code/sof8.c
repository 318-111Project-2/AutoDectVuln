/* have 2 stack overflow */

/* spend 43s */

#include <stdio.h>
#include <string.h>

#define MAXSIZE 10

void test(char *str){
	char buf[MAXSIZE];
	strcpy(buf, str); //bad
	printf("results: %s\n", buf);
}

int main(int argc, char **argv){
	char userstr[MAXSIZE];
	scanf("%s", userstr);
	test(userstr);
	
	return 0;
}