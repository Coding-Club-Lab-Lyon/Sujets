char *my_rotate_alpha(char *word)
{
    int c = 0;

    for (int i = 0; word[i]; i++) {
        if (word[i] > 122 || word[i] < 97)
            break;
        c = word[i] + (word[i] - 97);
        if (c > 122)
            c = 97 + (c - 122);
        word[i] = (char)c;
    }
    return word;
}

// deux matelas + deux chaises + table + cmaping gaz + poele + casserole + couvert + ralonge
