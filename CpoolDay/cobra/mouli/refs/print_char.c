#include <unistd.h>

void print_char(char c)
{
    write(1, &c, 1);
}
