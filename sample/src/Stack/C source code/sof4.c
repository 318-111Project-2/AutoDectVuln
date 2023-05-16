/* have 2 stackoverflows */

/* spend 39s */

#include <stdio.h>
#include <string.h>

#define	MAXSIZE		40
void
test(char *str)
{
	char buf[MAXSIZE];

	strncpy(buf, str, 80);			/* BAD */
	buf[MAXSIZE-1] = '\0';
	printf("result: %s\n", buf);
}

int
main(int argc, char **argv)
{
	char userstr[MAXSIZE];
	scanf("%s",userstr);
	test(userstr);

	return 0;
}