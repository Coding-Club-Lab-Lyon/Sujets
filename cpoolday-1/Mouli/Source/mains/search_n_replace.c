#include <stdio.h>
#include <unistd.h>

void search_n_replace(char *str, char a, char b);

void my_putstr_FORTESTING(char *s)
{
    int i = -1;

    while (s[++i])
        write(1, &s[i], 1);
}

void newline(void)
{
    write(1, "\b", 1);
}

int main(int argc, char *argv[])
{
    char test1[] = "EPITECH";
    char test2[] = "668";
    char test3[] = "EPITECH_OWO_nojdf_wefm_tteesst_zzaaaz_vanourilebg";
    char test4[] = "";
    char test5[] = "MATHIAS EST TRES TRES BEAU";

    my_putstr_FORTESTING("$[Basic]%");
    search_n_replace(test1, 'E', 'e');

    my_putstr_FORTESTING("$[Numbers]%");
    search_n_replace(test2, '7', '8');

    my_putstr_FORTESTING("$[Special characters]%");
    search_n_replace(test3, '_', '-');

    my_putstr_FORTESTING("$[Empty]%");
    search_n_replace(test4, 'E', 'e');

    my_putstr_FORTESTING("$[Nothing to replace]%");
    search_n_replace(test5, '#', 'e');
    return 0;
}
