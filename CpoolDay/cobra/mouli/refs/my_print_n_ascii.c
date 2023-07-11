void print_char(char c);

void my_print_n_ascii(int how_many)
{
    if (how_many > 94 || how_many < 0)
        return;
    for (char c = '!'; c < how_many + '!'; c++)
        print_char(c);
}
