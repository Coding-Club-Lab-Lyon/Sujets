#include <unistd.h>

int not_seen_before(char *s, int max_pos, char c)
{
    int i;

    i = -1;
    while (++i < max_pos)
        if (s[i] == c)
            return (0);
    return (1);
}

void my_union(char *s1, char *s2)
{
    int i = -1;
    int j = -1;

    i = -1;
    while (s1[++i])
        if (not_seen_before(s1, i, s1[i]))
            write(1, &s1[i], 1);
    while (s2[++j])
        if (not_seen_before(s1, i, s2[j]) & not_seen_before(s2, j, s2[j]))
            write(1, &s2[j], 1);
}
