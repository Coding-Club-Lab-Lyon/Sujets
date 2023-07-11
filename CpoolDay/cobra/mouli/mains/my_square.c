#include <stdlib.h>
#include <stdio.h>

int my_square(int number);

int main(int ac, char **av)
{
    fprintf(stdout, "%d\n", my_square(atoi(av[1])));
    return 0;
}
