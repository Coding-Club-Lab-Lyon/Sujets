#include <stdlib.h>

void my_print_n_ascii(int value);

int main(int ac, char **av)
{
    my_print_n_ascii(atoi(av[1]));
    return 0;
}
