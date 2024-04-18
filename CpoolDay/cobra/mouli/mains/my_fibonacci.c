#include <stdio.h>

void my_fibonacci(int minimum, int maximum);

int main(int ac, char *av[])
{
    if (ac != 3)
        return 0;
    my_fibonacci(atoi(av[1]), atoi(av[2]));
    return 0;
}
