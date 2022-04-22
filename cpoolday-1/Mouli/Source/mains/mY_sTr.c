#include <stdio.h>
#include <unistd.h>

void mY_sTr(char *str);

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
    mY_sTr("simple test");
    newline();

    my_putstr_FORTESTING("$[One out of two]%");
    mY_sTr("zYxWvUtSrQpOnMlKjIhGfEdCbA");
    newline();

    my_putstr_FORTESTING("$[Numbers and specials]%");
    mY_sTr("Salut les BOY 45-8 haha KEKW shrek.__d");
    newline();

    my_putstr_FORTESTING("$[Empty]%");
    mY_sTr("");
    newline();
    return 0;
}
