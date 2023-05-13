#include <stdio.h>
#include <stdlib.h>

int main(){
    char * x = malloc(4);
    free(x);
    return *x;
}