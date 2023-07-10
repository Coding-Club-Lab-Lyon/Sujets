void print_char(char c);

int isSeparator(char c)
{
    if (c == ' ' || c == '\t' || c == ',')
        return 1;
    return 0;
}

int getValueIndex(char *dict, char *key)
{
    int index = 0;
    int keySize = ({int i = 0; for (; key[i]; i++){i = i;}; i;});

    for (int i = 0; dict[i]; i++) {
        if (!i || isSeparator(dict[i - 1]))
            for (int j = 0; key[j] && key[j] == dict[i]; j++, i++)
                j == keySize - 1 ? ({return i + 2;}) : 0;
        else
            i++;
    }
    return 0;
}

void my_get_value(char *dictionary, char *toFind)
{
    int indexValue;

    if (!(indexValue = getValueIndex(dictionary, toFind)))
        return;
    if (dictionary[indexValue - 1] != ':' && dictionary[indexValue - 1] != '=')
        return;
    while (dictionary[indexValue] && !isSeparator(dictionary[indexValue]))
        print_char(dictionary[indexValue++]);
    print_char('\n');
}
