#include <unistd.h>

int iter(char *str, char c, int len)
{
    int i;

    i = 0;
    while (str[i] && (i < len || len == -1))
        if (str[i++] == c)
            return (1);
    return (0);
}

void inter(char *s1, char *s2)
{
    int i = 0;
    while (s1[i]) {
        if (!iter(s1, s1[i], i) && iter(s2, s1[i], -1))
            write(1, &s1[i], 1);
        i++;
    }
    write(1, "\n", 1);
}
