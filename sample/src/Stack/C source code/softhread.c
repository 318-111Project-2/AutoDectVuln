/*
  PLOVER: BUFF.OVER
 */

/*
  Unprotected string copy, unlocked shared resource, realpath with fixed buffer
*/

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFSIZE 5

void *foo(void* targ)
{

  char *buffer = ((char **)targ)[0];
  char *str =  ((char **)targ)[1];


  realpath(str, buffer);
  printf("results: %s\n", buffer);

  
  pthread_exit(NULL);
}

void *bar(void* targ)
{
  char **buffer = (char **)targ;
  
  *buffer = NULL;

  pthread_exit(NULL);
}

int main(int argc, char *argv[])
{
  char buf[BUFSIZE];
  pthread_t tids[2];
  char *tin[2];
  tin[0] = buf;
  if(argc > 1)
    tin[1] = argv[1];
  else
    return 0;

  int rc = pthread_create(&tids[0], NULL, foo, (void *)tin);
  rc = pthread_create(&tids[1], NULL, bar, (void *)&buf);
  pthread_join(tids[0],NULL);
  pthread_join(tids[1],NULL);

  printf("final string: %s \n", buf);

  return 0;
}

/* have 2 stackoverflows */
/* False negative*/
