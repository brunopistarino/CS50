#include <stdio.h>
#include <cs50.h>

int main(void)
{
    bool every_other = false;
    int r = 0;
    int digits = 0;
    long input = get_long("Number: ");
    long n = input;

    while (n > 0)
    {
        digits++;
        int a = n % 10;
        n = (n - a) / 10;

        if (every_other == true)
        {
            int x = a * 2;
            if (x < 10)
            {
                r += x;
            }
            else
            {
                int y = x % 10;
                r += y;
                r += (x - y) / 10;
            }

            every_other = false;
        }
        else
        {
            r += a;
            every_other = true;
        }
    }
    if (r % 10 == 0)
    {
        if (digits == 15 && (input / 10000000000000 == 34 || input / 10000000000000 == 37))
        {
            printf("AMEX\n");
        }
        else if (digits == 16 && (input / 100000000000000 == 51 || input / 100000000000000 == 52 || input / 100000000000000 == 53
                                  || input / 100000000000000 == 54 || input / 100000000000000 == 55))
        {
            printf("MASTERCARD\n");
        }
        else if ((digits == 13 && input / 1000000000000 == 4) || (digits == 16 && input / 1000000000000000 == 4))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}