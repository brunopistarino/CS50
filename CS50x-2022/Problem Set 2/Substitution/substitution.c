#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];

    if (strlen(key) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    for (int i = 0; i < 26; i++)
    {
        key[i] = toupper(key[i]);
        char c = key[i];

        if (!isalpha(c))
        {
            printf("Key must only contain alphabetic characters.\n");
            return 1;
        }

        for (int x = i + 1; x < 26; x++)
        {
            if (key[i] == key[x])
            {
                printf("Key must not contain repeated characters\n");
                return 1;
            }
        }
    }

    string plain = get_string("plaintext:  ");
    int plainl = strlen(plain);
    char r[256] = "\0";

    for (int i = 0; i < plainl; i++)
    {
        char c = plain[i];

        if (isalpha(c))
        {
            if (isupper(c))
            {
                r[i] = key[c - 65];
            }
            else
            {
                r[i] = tolower(key[toupper(c) - 65]);
            }
        }
        else
        {
            r[i] = c;
        }
    }

    printf("ciphertext: %s\n", r);
}