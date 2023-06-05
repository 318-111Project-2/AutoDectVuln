/* have 2 stack overflow */

/* spend 16s */

#include <stdio.h>
#include <string.h>

#define	MAXSIZE		40
void
test(char *str)
{
	char buf[MAXSIZE];

	snprintf(buf, 1024, "<%s>", str);	/* OK */
	printf("result: %s\n", buf);
}

int
main(int argc, char **argv)
{
	/* overly long constant string */
	char a[40];
    scanf("%s",a);
	test(a);
	return 0;
}