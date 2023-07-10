void print_char(char c);

void my_get_words(char *sentance)
{
    for (int i = 0; sentance[i]; i++) {
        while (sentance[i] == ' ' || sentance[i] == '\t' && sentance[i])
            i++;
        while (sentance[i] != ' ' && sentance[i] != '\t' && sentance[i])
            print_char(sentance[i++]);
        if (sentance[i])
            print_char('\n');
    }
}
