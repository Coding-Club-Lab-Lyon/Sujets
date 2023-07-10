#include <stdio.h>

char *my_rotate_alpha(char *word);

int main(int ac, char **av)
{
    fprintf(stdout, "%s\n", my_rotate_alpha(av[1]));
}