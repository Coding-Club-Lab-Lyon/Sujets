int my_little_bistro(int value1, char op, int value2)
{
    if ((op == '/' || op == '%') && !value2)
        return 0;
    switch (op) {
        case '+': return value1 + value2;
        case '-': return value1 - value2;
        case '*': return value1 * value2;
        case '/': return value1 / value2;
        case '%': return value1 % value2;
        default: return 0;
    }
}
