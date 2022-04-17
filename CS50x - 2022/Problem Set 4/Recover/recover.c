#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// Block size
#define BLOCK 512
typedef uint8_t  BYTE;

bool isJPEG(BYTE buffer[BLOCK]);

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover file\n");
        return 1;
    }

    FILE *inptr = fopen(argv[1], "r");
    if (inptr == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }

    BYTE buffer[BLOCK];
    bool newImg = false;
    int count = -1;
    FILE *img[50];
    char filename[7];

    while (fread(&buffer, BLOCK, 1, inptr))
    {
        if (isJPEG(buffer))
        {
            if (count > -1)
            {
                fclose(img[count]);
            }

            count++;
            sprintf(filename, "%03i.jpg", count);
            newImg = true;

            img[count] = fopen(filename, "w");
            fwrite(buffer, BLOCK, 1, img[count]);
        }

        if (newImg == false && count > -1)
        {
            fwrite(buffer, BLOCK, 1, img[count]);
        }

        newImg = false;
    }

    fclose(inptr);
}

bool isJPEG(BYTE buffer[BLOCK])
{
    if (buffer[0] == 0xff)
    {
        if (buffer[1] == 0xd8)
        {
            if (buffer[2] == 0xff)
            {
                if (buffer[3] >= 0xe0 && buffer[3] <= 0xef)
                {
                    return true;
                }
            }
        }
    }

    return false;
}