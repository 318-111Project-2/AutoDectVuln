/* have 3 heap overflows */

/* spend 9-13s */

/* Link https://samate.nist.gov/SARD/test-cases/1632/versions/1.0.0 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define	MAXSIZE		40
void
test(char *str1, char *str2)
{
	char *buf, *p;
	int l, x;

	buf = malloc(MAXSIZE);
	if(!buf)
		return;
	p = buf;
	l = MAXSIZE;

	//snprintf(p, l, "%s", str1);
	x = strlen(p);
	p += x;
	l -= x;

	/* there's no check on the length here */
	*p++ = ' ';					/* BAD */
	*p++ = '-';					/* BAD */
	l -= 2;						/* BAD */

	/* now length may be negative */
	//snprintf(p, l, "%s", str2);			/* BAD */
	x = strlen(p);
	p += x;
	l -= x;

	printf("result: %s\n", buf);
	free(buf);
}

int
main(int argc, char **argv)
{
	char *userstr, *userstr2;
    /*scanf("%s",userstr);
	scanf("%s",userstr2);
    userstr = argv[1];
	userstr2 = argv[2];*/
	//test(userstr, userstr2);
	if( scanf("%s",userstr),
	scanf("%s",userstr2)) {
		userstr = argv[1];
		userstr2 = argv[2];
		test(userstr, userstr2);
	}
	return 0;
}