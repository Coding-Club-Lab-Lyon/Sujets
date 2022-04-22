#include <stdio.h>
#include <unistd.h>

void my_union(char *s1, char *s2);

void my_putstr_FORTESTING(char *s)
{
    int i = -1;

    while (s[++i])
        write(1, &s[i], 1);
}

void newline(void)
{
    write(1, "\n", 1);
}

int main(int argc, char *argv[])
{
    my_putstr_FORTESTING("$[Basic]%");
    my_union("EPITECH", "BASIC");

    my_putstr_FORTESTING("$[Subject test]%");
    my_union("rien", "cette phrase ne cache rien");

    my_putstr_FORTESTING("$[Simple test]%");
    my_union("vavari8er", "p4labanier");

    my_putstr_FORTESTING("$[Numbers and specials]%");
    my_union("for pony 754 48 /",
    "qwertyuiopasdfghjklzxcvbnm123456789<>/:;'[]{}|_=+-*^%#@!`~");

    my_putstr_FORTESTING("$[Empty]%");
    my_union("", "");
    return 0;
}
