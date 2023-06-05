
/*Link  https://samate.nist.gov/SARD/test-cases/1561/versions/1.0.0*/ 

/*have 1 format string bug */

/*spend 12s*/
#include <stdio.h>

char *fmts[] = {
	"<%s>\n",
	"[%s]\n",
};

void test(char *str)
{
	int idx;

	idx = (str[0] == '!');
	printf(fmts[idx], str);				/* bad */
}

int main(int argc, char **argv)
{
	char *userstr;
	scanf("%s",userstr);
	test(userstr);
	return 0;
}