/* have 2 stackoverflow */

/* spend 46s */

#include <stdio.h>
#include <string.h>

#define	MAXSIZE		40

char * shortstr(char *p, int n, int targ)
{
	if(n > targ)
		return shortstr(p+1, n-1, targ);
	return p;
}

void test(char *str)
{
	char buf[MAXSIZE], *str2;

	str2 = shortstr(str, strlen(str), 80);
	strcpy(buf, str2);				/* BAD */
	printf("result: %s\n", buf);
}

int main(int argc, char **argv)
{
	char userstr[MAXSIZE];
	scanf("%s",userstr);
	test(userstr);
	return 0;
}