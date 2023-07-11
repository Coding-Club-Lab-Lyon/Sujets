void my_print_revert(char *to_revert);

int main(int ac, char **av)
{
    my_print_revert(av[1]);
    return 0;
}
