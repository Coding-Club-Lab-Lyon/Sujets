#include <unistd.h>

static void my_putstr(char *str)
{
    int i = 0;

    while (str[i] != '\0')
        write(1, &str[i++], 1);
}

void search_n_replace(char *str, char a, char b)
{
    int i = 0;

    while (str[i]) {
        if (str[i] == a)
            str[i] = b;
        i++;
    }
    my_putstr(str);
    my_putstr("\n");
}