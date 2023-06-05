#include <stdio.h>
#include <string.h>

#define	MAXSIZE		40
void test(char *str)
{
	char buf[MAXSIZE];

	/* this is a failed attempt at fixing the bug 
	 * %35s does not limit the output length to 35
	 */
	snprintf(buf, 1024, "<%35s>", str);	/* BAD */
	printf("result: %s\n", buf);
}

int main(int argc, char **argv)
{
	char *userstr;
	userstr = argv[1];
	test(userstr);
	return 0;
}