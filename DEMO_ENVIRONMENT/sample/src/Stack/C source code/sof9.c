/* have 2 stack overflow */

/* spend 33s */

#include <stdio.h>
#include <string.h>

#define	MAXSIZE		40

void test(char *str)
{
	char buf[MAXSIZE];

	if(strlen(str) > MAXSIZE)
		return;
	strcpy(buf, str);			   
	printf("result: %s\n", buf);
}

int main(int argc, char **argv)
{
	char userstr[MAXSIZE];
    scanf("%s",userstr);
	test(userstr);
	return 0;
}