#include <stdio.h>

char *my_replace_char(char *origin, char toFind, char toRelace);

int main(int ac, char **av)
{
    fprintf(stdout, "%s\n", my_replace_char(av[1], av[2][0], av[3][0]));
    return 0;
}
