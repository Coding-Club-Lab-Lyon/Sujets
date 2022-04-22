#include <stdio.h>
#include <unistd.h>

int hidentf_order(char *s1, char *s2)
{
    int i = -1;
    int j = 0;

    while (s2[++i])
        if (s1[j] == s2[i])
            j++;
    return (!s1[j]);
}