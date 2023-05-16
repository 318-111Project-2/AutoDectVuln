/* have 2 stack overflow */

/* spend 77s */


#include <stdio.h>
#include <string.h>

#define	MAXSIZE		40
void test(void)
{
	char buf[MAXSIZE];

	if(fgets(buf, 1024, stdin))			/* BAD */
		printf("result: %s\n", buf);
}

int main(int argc, char **argv)
{
	test();
	return 0;
}
