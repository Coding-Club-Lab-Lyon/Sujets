void print_char(char c);

void my_print_ascii(void)
{
    char c = 33;

    while (c <= 126) {
        print_char(c);
        c++;
    }
}
