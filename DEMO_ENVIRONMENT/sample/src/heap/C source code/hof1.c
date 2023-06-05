/* have 2 heap overflow */

/* spend 26s */

/* Link https://samate.nist.gov/SARD/test-cases/1628/versions/1.0.0 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define	MAXSIZE		40
void
test(char *str)
{
	char *buf;

	buf = malloc(MAXSIZE);
	if(!buf)
		return;
	strcpy(buf, str);				/* BAD */
	printf("result: %s\n", buf);
	free(buf);
}

int
main(int argc, char **argv)
{
	char *userstr;
    scanf("%s",userstr);
    userstr = argv[1];
	test(userstr);
	if(argc > 1) {
		userstr = argv[1];
		test(userstr);
	}
	return 0;
}

