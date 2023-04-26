/*
  PLOVER: BUFF.OVER
*/

/*
	No bounds checking
*/

#include <stdio.h>
#include <string.h>

#define MAXSIZE 10

void test(char *str){
	char buf[MAXSIZE];
	strcpy(buf, str); //bad
	printf("results: %s\n", buf);
}

int main(int argc, char **argv){
	char *userstr;
	userstr = argv[1];
	test(userstr);
	
	return 0;
}

/* have 2 stackoverflow */
