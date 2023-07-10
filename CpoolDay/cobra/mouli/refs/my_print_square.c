void print_char(char c);

void my_print_square(int size, char c)
{
    if (size <= 1 || !(c >= 33 && c <= 126))
        return;
    for (int i = 0; i < size; i++)
        print_char(c);
    print_char('\n');
    for (int i = 1; i < size - 1; i++) {
        print_char(c);
        for (int j = 1; j < size - 1; j++)
            print_char(' ');
        print_char(c);
        print_char('\n');
    }
    for (int i = 0; i < size; i++)
        print_char(c);
}
