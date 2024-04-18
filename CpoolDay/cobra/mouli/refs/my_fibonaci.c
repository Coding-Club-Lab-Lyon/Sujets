#include <stdio.h>

void my_fibonacci(int minimum, int maximum)
{
    int n, first = 0, second = 1, next, c;

    if (minimum > maximum || minimum == maximum)
        return;
    for (c = 0; next <= maximum; c++) {
        if (c <= 1)
            next = c;
        else {
            next = first + second;
            first = second;
            second = next;
        }
        if (next >= minimum && next <= maximum)
            fprintf(stdout, "%d\n", next);
    }
}
