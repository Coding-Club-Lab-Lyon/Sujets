void print_char(char c);

void my_get_words(char *sentance)
{
    int start = 0;
    int begin = 1;

    for (int i = 0; sentance[i]; ++i) {
        if (((sentance[i] >= 'A') && (sentance[i] <= 'Z')) ||
            ((sentance[i] >= 'a') && (sentance[i] <= 'z'))) {
            (!start && !begin) ? print_char('\n') : 0;
            print_char(sentance[i]);
            start = 1;
            begin = 0;
        } else {
            start = 0;
        }
    }
}
