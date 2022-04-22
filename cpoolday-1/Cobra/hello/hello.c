#include <unistd.h>

void hello(void)
{
    write(1, "Hello, World!\n", 14);
}