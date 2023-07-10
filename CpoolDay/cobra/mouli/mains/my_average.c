#include <stdio.h>
#include <stdlib.h>

float my_average(int *grades, int count);

int main(int ac, char **av)
{
    int *list = malloc(sizeof(int) * (ac - 1));

    for (int i = 1; i < ac; i++)
        list[i - 1] = atoi(av[i]);
    fprintf(stdout, "%f\n", my_average(list, ac - 1));
    return 0;
}
