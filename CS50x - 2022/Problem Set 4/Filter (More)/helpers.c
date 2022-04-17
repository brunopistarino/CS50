#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            uint8_t t = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = image[i][j].rgbtGreen = image[i][j].rgbtRed = t;
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE tmp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = tmp;
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmp[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sumRed = 0, sumGreen = 0, sumBlue = 0;
            float sumCount = 0.0;

            for (int x = -1; x < 2; x++)
            {
                for (int y = -1; y < 2; y++)
                {
                    int rx = i + x, ry = j + y;

                    if ((rx >= 0 && rx < height) && (ry >= 0 && ry < width))
                    {
                        sumRed += image[rx][ry].rgbtRed;
                        sumGreen += image[rx][ry].rgbtGreen;
                        sumBlue += image[rx][ry].rgbtBlue;
                        sumCount++;
                    }
                }
            }

            tmp[i][j].rgbtRed = round(sumRed / sumCount);
            tmp[i][j].rgbtGreen = round(sumGreen / sumCount);
            tmp[i][j].rgbtBlue = round(sumBlue / sumCount);
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = tmp[i][j];
        }
    }

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    int xArray[9] = {-1, 0, 1, -2, 0, 2, -1, 0, 1};
    int yArray[9] = {-1, -2, -1, 0, 0, 0, 1, 2, 1};
    RGBTRIPLE tmp[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int GxRed = 0, GxGreen = 0, GxBlue = 0, GyRed = 0, GyGreen = 0, GyBlue = 0, arrayCount = -1;

            for (int x = -1; x < 2; x++)
            {
                for (int y = -1; y < 2; y++)
                {
                    arrayCount++;
                    int rx = i + x, ry = j + y;

                    if ((rx >= 0 && rx < height) && (ry >= 0 && ry < width))
                    {
                        GxRed += image[rx][ry].rgbtRed * xArray[arrayCount];
                        GxGreen += image[rx][ry].rgbtGreen * xArray[arrayCount];
                        GxBlue += image[rx][ry].rgbtBlue * xArray[arrayCount];

                        GyRed += image[rx][ry].rgbtRed * yArray[arrayCount];
                        GyGreen += image[rx][ry].rgbtGreen * yArray[arrayCount];
                        GyBlue += image[rx][ry].rgbtBlue * yArray[arrayCount];
                    }
                }
            }

            int rRed = round(sqrt(GxRed * GxRed + GyRed * GyRed));
            int rGreen = round(sqrt(GxGreen * GxGreen + GyGreen * GyGreen));
            int rBlue = round(sqrt(GxBlue * GxBlue + GyBlue * GyBlue));

            tmp[i][j].rgbtRed = (rRed > 255) ? 255 : rRed;
            tmp[i][j].rgbtGreen = (rGreen > 255) ? 255 : rGreen;
            tmp[i][j].rgbtBlue = (rBlue > 255) ? 255 : rBlue;
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = tmp[i][j];
        }
    }

    return;
}