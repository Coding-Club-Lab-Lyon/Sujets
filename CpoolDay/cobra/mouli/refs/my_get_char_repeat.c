int my_get_char_repeat(char to_find, char *to_search)
{
    int ret = 0;

    for (int i = 0; to_search[i]; i++)
        ret += to_search[i] == to_find ? 1 : 0;
    return ret;
}
