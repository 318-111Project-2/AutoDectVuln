/*
     gcc no_fmt.c -o no_fmt -fcf-protection=none -fno-stack-protector
*/
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

bool check_fmt(char *buffer, char *fmt) {
    if (strlen(fmt) >= sizeof(buffer)) {
        return false;
    }
    else {
        return true;
    }
}

int main() {
    char buffer[10];
    int num = 69;
    char fmt[10];

    // Use scanf to read the format string from user input
    scanf("%9s", fmt);

    // Check the format string
    if (check_fmt(buffer, fmt)) {
        // The format string is safe, so use printf to print the value to the buffer
        snprintf(buffer, sizeof(buffer), fmt, num);
        printf("%s", buffer);
    }

    return 0;
}
