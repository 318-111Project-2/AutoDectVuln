/*PLOVER: BUFF.OVER, BUFF.FORMAT*/


/*
Description: A strcpy of a buffer with a missing NUL character causes a stack buffer to overflow.
Keywords: Size0 Complex1 BufferOverflow Stack Strcpy NoNul
ValidArg: "a"*30
InvalidArg: "a"*100
*/

#include <stdio.h>
#include <string.h>

/* 
 * we pick a round buffer size in hopes that the compiler lays these
 * out next to each other without padding.  Other layouts may
 * inadvertantly NUL terminate the buffer with stack garbage.
 */
#define	MAXSIZE		32
#define	MAXSIZE1	40
#define MAXSIZE2 	10
void test(char *str)
{
	char buf3[MAXSIZE];
	char buf2[MAXSIZE];
	char buf1[MAXSIZE];

	/* strncpy does not NUL terminate if buffer isnt large enough */
	strncpy(buf1, str, sizeof buf1);
	strncpy(buf2, "This is a Test string", sizeof buf2);
	strcpy(buf3, buf1);			/* BAD */
	printf("result: %s\n", buf3);
}

void test1(void)
{
	char buf[MAXSIZE1];

	if(fgets(buf, 1024, stdin))			/* BAD */
		printf("result: %s\n", buf);
}
void test2(void)
{
	char buf2[MAXSIZE];
	char buf1[MAXSIZE];
	int n;

	/* read does not NUL terminate */
	n = read(0, buf1, sizeof buf1);
	strcpy(buf2, buf1);				/* BAD */
	printf("result: %s\n", buf2);
}

void test3(char *str)
{
	char buf[MAXSIZE1];

	snprintf(buf, 1024, "<%s>", str);	/* OK */
	printf("result: %s\n", buf);
}

void test4(char *str)
{
	char buf[MAXSIZE1];

	/* this is a failed attempt at fixing the bug 
	 * %35s does not limit the output length to 35
	 */
	snprintf(buf, 1024, "<%35s>", str);	/* BAD */
	printf("result: %s\n", buf);
}

void test5(char *str){
	char buf[MAXSIZE2];
	strcpy(buf, str); //bad
	printf("results: %s\n", buf);
}

void test6(char *str)
{
	char buf[MAXSIZE1];

	if(strlen(str) > MAXSIZE1)
		return;
	strcpy(buf, str);	// bad		   
	printf("result: %s\n", buf);
}

int  main(int argc, char **argv)
{
	char *userstr;
	userstr = argv[1];
	test(userstr);
	test1();
	test2();
	char a[40];
    scanf("%s",a);
	test3(a);
	test4(userstr);
	test5(userstr);
	test6(userstr);
	return 0;
}

/*have 8 stackoverflows*/

