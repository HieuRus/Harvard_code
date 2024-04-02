#include "helpers.h"
#include <stdio.h>

void colorize(int height, int width, RGBTRIPLE image[height][width])
{
    // Change all black pixels to a color of your choosing
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            RGBTRIPLE pixel = image[h][w];
            if (pixel.rgbtRed == 0 && pixel.rgbtGreen == 0 && pixel.rgbtBlue == 0)  //check black pixel and replace it with desired color
            {
                pixel.rgbtRed = 153;
                pixel.rgbtGreen = 50;
                pixel.rgbtBlue = 204;
                image[h][w] = pixel;
            }
        }
    }
}
