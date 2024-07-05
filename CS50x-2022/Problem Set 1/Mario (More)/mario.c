#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (!(n >= 1 && n <= 8));

    for (int i = 0; i < n; i++)
    {
        for (int x = 0; x < n; x++)
        {
            if (n - (i + 2) < x)
            {
                printf("#");
            }
            else
            {
                printf(" ");
            }
        }

        printf("  ");

        for (int x = 0; x < n; x++)
        {
            if (!(i < x))
            {
                printf("#");
            }
        }

        printf("\n");
    }
}