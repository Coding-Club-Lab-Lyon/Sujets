#include <stdlib.h>

void my_print_square(int size, char c);

int main(int ac, char **av)
{
    my_print_square(atoi(av[1]), av[2][0]);
    return 0;
}
