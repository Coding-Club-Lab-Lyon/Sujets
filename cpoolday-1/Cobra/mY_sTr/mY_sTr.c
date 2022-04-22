#include <unistd.h>

void my_putchar(char c)
{
    write(1, &c, 1);
}

void mY_sTr(char *str)
{
    int i = -1;

    while (str[++i])
        if (str[i] >= 'a' && str[i] <= 'z')
            my_putchar(str[i] - 32);
        else if (str[i] >= 'A' && str[i] <= 'Z')
            my_putchar(str[i] + 32);
        else
            my_putchar(str[i]);
}
