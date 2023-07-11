void print_char(char c);

void my_print_revert(char *to_revert)
{
    int index = 0;

    while(to_revert[index])
        index++;
    for (; index >= 0; index--)
        print_char(to_revert[index]);
}
