/* have 2 stack overflows */

/* spend 10s */


#include <stdio.h>
#include <string.h>

#define	MAXSIZE		40
void
test(char *str)
{
	char buf[MAXSIZE];

	snprintf(buf, 1024, "<%s>", str);	/* BAD */
	printf("result: %s\n", buf);
}

int
main(int argc, char **argv)
{
	char *userstr;
	userstr = argv[1];
	test(userstr);
	return 0;
}