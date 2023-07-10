void print_char(char c);

void my_print_n_ascii(int howMany)
{
    if (howMany > 94 || howMany < 0)
        return;
    for (char c = 33; c < howMany + 33; c++)
        print_char(c);
}
