#include <stdio.h>
#include <stdlib.h>

int my_exp(int value, int exp);

int main(int ac, char **av)
{
    fprintf(stdout, "%d\n", my_exp(atoi(av[1]), atoi(av[2])));
    return 0;
}
