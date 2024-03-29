/* have 1 stack overflow */

/* spend 36s */

#include <stdio.h>
#include <string.h>

/* 
 * we pick a round buffer size in hopes that the compiler lays these
 * out next to each other without padding.  Other layouts may
 * inadvertantly NUL terminate the buffer with stack garbage.
 */
#define	MAXSIZE		32

void test(char *str)
{
	char buf3[MAXSIZE];
	char buf2[MAXSIZE];
	char buf1[MAXSIZE];

	/* strncpy does not NUL terminate if buffer isnt large enough */
	strncpy(buf1, str, sizeof buf1);
	strncpy(buf2, "This is a Test string", sizeof buf2);
	strcpy(buf3, buf1);			/* BAD */
	printf("result: %s\n", buf3);
}

int main(int argc, char **argv)
{
	char userstr[MAXSIZE];
	scanf("%s",userstr);
	test(userstr);
	
	return 0;
}



