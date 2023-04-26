/*
  PLOVER: BUFF.OVER, NUM.OBO
*/
/*
	Off-by-one
*/

#include <stdio.h>
#include <string.h>

#define MAXSIZE 5

void test(char *str){
	char buf[MAXSIZE];
	strncpy(buf, str, MAXSIZE);
	printf("results: %s\n", buf); //bad
}

int main(int argc, char **argv){
	char *userstr;
    	char a[MAXSIZE];
    	scanf("%s",a);
	test(userstr);
	return 0;
}

/* have 1 stackoverflow */
