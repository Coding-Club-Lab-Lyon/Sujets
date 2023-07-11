#include <stdlib.h>

void my_sort(int *nlist, int size);

int main(int ac, char **av)
{
    int *nlist = malloc(sizeof(int *) * (ac - 1));

    for (int i = 1; i < ac; i++)
        nlist[i - 1] = atoi(av[i]);
    my_sort(nlist, ac - 1);
    free(nlist);
    return 0;
}
