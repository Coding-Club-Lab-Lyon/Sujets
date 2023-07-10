#include <stdio.h>
#include <stdlib.h>

int my_little_bistro(int value1, char op, int value2);

int main(int ac, char **av)
{
    printf("%d\n", my_little_bistro(atoi(av[1]), av[2][0], atoi(av[3])));
    return 0;
}