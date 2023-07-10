#include <stdio.h>

int my_get_char_repeat(char to_find, char *to_search);

int main(int ac, char **av)
{
    fprintf(stdout, "%d\n", my_get_char_repeat(av[1][0], av[2]));
    return 0;
}