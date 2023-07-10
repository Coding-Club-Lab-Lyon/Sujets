

int my_exp(int value, int exp)
{
    int res = value;

    if (exp == 0)
        return value > 0 ? 1 : -1;
    for (int i = 0; i < exp - 1; i++)
        res *= value;
    return res;
}
