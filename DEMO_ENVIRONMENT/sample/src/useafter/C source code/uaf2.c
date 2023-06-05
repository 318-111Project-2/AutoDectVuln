/* have 1 heap overflow 1 use after free */

/* spend 2s */

/* Link https://samate.nist.gov/SARD/test-cases/1476/versions/1.0.0 */


#include <stdio.h>
#include <stdlib.h>

int main(){
    char * x = malloc(4);
    free(x);
    return *x;
}