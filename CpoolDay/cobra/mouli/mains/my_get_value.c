#include <stdio.h>

void my_get_value(char *dictionary, char *toFind);

int main(int ac, char **av)
{
    my_get_value(av[1], av[2]);
    return 0;
}
