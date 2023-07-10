void print_char(char c);

void my_print_revert(char *toRevert)
{
    int index = 0;

    while(toRevert[index])
        index++;
    for (; index >= 0; index--)
        print_char(toRevert[index]);
}
