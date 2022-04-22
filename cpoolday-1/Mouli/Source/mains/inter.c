#include <stdio.h>
#include <unistd.h>

void inter(char *s1, char *s2);

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
    my_putstr_FORTESTING("$[Simple test]%");
    inter("EPITECH", "BASIC");

    my_putstr_FORTESTING("$[Subject test]%");
    inter("rien", "cette phrase ne cache rien");

    my_putstr_FORTESTING("$[Medium test]%");
    inter("vavari8er", "p4labanier");

    my_putstr_FORTESTING("$[Numbers and specials]%");
    inter("for pony 754 48 /",
    "qwertyuiopasdfghjklzxcvbnm123456789<>/:;'[]{}|_=+-*^%#@!`~");

    my_putstr_FORTESTING("$[Empty]%");
    inter("", "");
    return 0;
}
