#include <stdlib.h>
#include <stdio.h>
#include <string.h>

typedef struct str_t str;
struct str_t {
	union {
		int   a;
		char *b;
	} foo;
};

int main(int argc, char *argv[])
{
	str container;
	container.foo.a = 0;
	
	if ((container.foo.b = (char *)malloc(256*sizeof(char))) != NULL)
	{
		strcpy(container.foo.b, "Falut!");
		container.foo.b[0] = 'S';
		printf("%s\n", container.foo.b);
		free(container.foo.b);	

		if(container.foo.b)
			container.foo.b[0] = 'S';					/* FLAW */
	}
	return 0;
}