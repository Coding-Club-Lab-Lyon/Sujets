void print_number(int value);

void my_sort(int *nlist, int size)
{
    for (int i = 0; i + 1 < size; i++) {
        if (nlist[i] > nlist[i + 1]) {
            nlist[i] ^= nlist[i + 1];
            nlist[i + 1] ^= nlist[i];
            nlist[i] ^= nlist[i + 1];
            my_sort(nlist, size);
            return;
        }
    }
    for (int i = 0; i < size; i++)
        print_number(nlist[i]);
}
