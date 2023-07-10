float my_average(int *grades, int count)
{
    int all = 0;

    if (!count)
        return 0;
    for (int i = 0; i < count; i++)
        all >= 0 ? all += grades[i] : ({return -1;});
    return (float)all / (float)count;
}