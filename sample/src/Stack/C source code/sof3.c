/*PLOVER: BUFF.OVER, BUFF.FORMAT*/

/*
Description: A strcpy of a buffer with a missing NUL character causes a stack buffer to overflow.
Keywords: Size0 Complex0 BufferOverflow Stack Strcpy NoNul
ValidStream: "a"*20
InvalidStream: "a"*100
*/

#include <stdio.h>
#include <string.h>
#include <unistd.h>

/* 
 * we pick a round buffer size in hopes that the compiler lays these
 * out next to each other without padding.  Other layouts may
 * inadvertantly NUL terminate the buffer with stack garbage.
 */
#define	MAXSIZE		32

void
test(void)
{
	char buf2[MAXSIZE];
	char buf1[MAXSIZE];
	int n;

	/* read does not NUL terminate */
	n = read(0, buf1, sizeof buf1);
	strcpy(buf2, buf1);				/* BAD */
	printf("result: %s\n", buf2);
}

int
main(int argc, char **argv)
{
	test();
	return 0;
}

/* have 2 stackoverflow */

