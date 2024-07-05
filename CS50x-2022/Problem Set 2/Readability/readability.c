#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");

    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    float L = (float)letters / words * 100;
    float S = (float)sentences / words * 100;

    int r = round(0.0588 * L - 0.296 * S - 15.8);

    if (r > 16)
    {
        printf("Grade 16+\n");
    }
    else if (r < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", r);
    }
}

int count_letters(string text)
{
    int t = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        char c = text[i];

        if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z'))
        {
            t++;
        }
    }

    return t;
}

int count_words(string text)
{
    int t = 0;
    bool newWord = true;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        char c = text[i];

        if (newWord == true && isalpha(c))
        {
            t++;
            newWord = false;
        }
        else if (c == ' ')
        {
            newWord = true;
        }
    }

    return t;
}

int count_sentences(string text)
{
    int t = 0;
    bool newSentence = true;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        char c = text[i];

        if (newSentence == true && isalpha(c))
        {
            t++;
            newSentence = false;
        }
        else if (c == '.' || c == '!' || c == '?')
        {
            newSentence = true;
        }
    }

    return t;
}