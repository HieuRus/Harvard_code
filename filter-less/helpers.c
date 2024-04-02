#include "helpers.h"
#include <stdlib.h>
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            RGBTRIPLE pixel = image[h][w];
            double avgColorvalue = (double)((pixel.rgbtRed + pixel.rgbtGreen + pixel.rgbtBlue) / 3.0);
            int grayScale = round(avgColorvalue);
            pixel.rgbtRed = grayScale;
            pixel.rgbtGreen = grayScale;
            pixel.rgbtBlue = grayScale;
            image[h][w] = pixel;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            RGBTRIPLE pixel = image[h][w];
            double dsepiaRed = (0.393 * pixel.rgbtRed) + (0.769 * pixel.rgbtGreen) + (0.189 * pixel.rgbtBlue);
            double dsepiaGreen = (0.349 * pixel.rgbtRed) + (0.686 * pixel.rgbtGreen) + (0.168 * pixel.rgbtBlue);
            double dsepiaBlue = (0.272 * pixel.rgbtRed) + (0.534 * pixel.rgbtGreen) + (0.131 * pixel.rgbtBlue);

            if (dsepiaRed > 255)
            {
                dsepiaRed = 255;
            }
            if (dsepiaGreen > 255)
            {
                dsepiaGreen = 255;
            }
            if (dsepiaBlue > 255)
            {
                dsepiaBlue = 255;
            }
            int sepiaRed = round(dsepiaRed);
            int sepiaGreen = round(dsepiaGreen);
            int sepiaBlue = round(dsepiaBlue);
            pixel.rgbtRed = sepiaRed;
            pixel.rgbtGreen = sepiaGreen;
            pixel.rgbtBlue = sepiaBlue;
            image[h][w] = pixel;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int middle = trunc(width / 2);
    int rightIndex = width - 1;
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < middle; w++)
        {
            RGBTRIPLE leftPixel = image[h][w];
            RGBTRIPLE rightPixel = image[h][rightIndex - w];
            image[h][rightIndex - w] = leftPixel; // swap
            image[h][w] = rightPixel;             // swap
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE newImage[height][width]; // create 2 dimentional array to store the blur value

    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            double sumRed = 0;
            double sumGreen = 0;
            double sumBlue = 0;
            double totalPixels = 0;
            //algorithm to loop through only neighbor pixels-one column before after that pixel
            for (int h1 = h - 1; h1 <= h + 1; h1++)
            {
                if (h1 >= 0 && h1 < height) //make sure not out of image
                {
                    for (int w1 = w - 1; w1 <= w + 1; w1++)
                    {
                        if (w1 >= 0 && w1 < width)
                        {
                            RGBTRIPLE pixel = image[h1][w1];
                            totalPixels++;
                            sumRed += pixel.rgbtRed;
                            sumGreen += pixel.rgbtGreen;
                            sumBlue += pixel.rgbtBlue;
                        }
                    }
                }
            }
            double davgRed = sumRed / totalPixels;
            int avgRed = round(davgRed);
            double davgGreen = sumGreen / totalPixels;
            int avgGreen = round(davgGreen);
            double davgBlue = sumBlue / totalPixels;
            int avgBlue = round(davgBlue);
            newImage[h][w].rgbtRed = avgRed;
            newImage[h][w].rgbtGreen = avgGreen;
            newImage[h][w].rgbtBlue = avgBlue;
        }
    }
    // copy all pixels from newImage to image
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            RGBTRIPLE pixel = image[h][w];
            pixel.rgbtRed = newImage[h][w].rgbtRed; // copy the blur value to the original pic
            pixel.rgbtGreen = newImage[h][w].rgbtGreen;
            pixel.rgbtBlue = newImage[h][w].rgbtBlue;
            image[h][w] = pixel;
        }
    }
    return;
}
