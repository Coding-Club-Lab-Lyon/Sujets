void print_number(int value);

void my_fibonacci(int minimum, int maximum)
{
    int n, first = 0, second = 1, next = 0, c;

    if (minimum > maximum || minimum < 0)
        return;
    for (c = 0; next <= maximum; c++) {
        if (c <= 1)
            next = c;
        else {
            next = first + second;
            first = second;
            second = next;
        }
        if (next >= minimum && next <= maximum)
            print_number(next);
    }
}
