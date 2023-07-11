float my_average(int *grades, int count)
{
    float all = 0;

    if (!count)
        return 0;
    for (int i = 0; i < count; i++)
        all += grades[i];
    return all / (float)count;
}
