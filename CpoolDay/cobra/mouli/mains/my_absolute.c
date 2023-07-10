#include <stdio.h>
#include <stdlib.h>

int my_absolute(int value);

int main(int ac, char **av)
{
    fprintf(stdout, "%d\n", my_absolute(atoi(av[1])));
    return 0;
}