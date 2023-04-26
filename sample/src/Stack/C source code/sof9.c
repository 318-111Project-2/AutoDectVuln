/*PLOVER: BUFF.OVER, NUM.OBO*/

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

int
main(int argc, char **argv)
{
	char *userstr;

	char a[MAXSIZE];
    	scanf("%s",a);
	test(a);
	return 0;
}

/* have 2 stackoverflow */
