#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Please input the height (1 to 8): ");
    }
    while (height < 1 || height > 8); // varify user input

    // r stands for row
    for (int r = 0; r < height; r++)
    {
        // c stands for column
        for (int c = 0; c < height; c++)
        {
            // height - r -1 is number of spaces. subtract 1 to offset 0 index
            if (c < height - r - 1)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }

        printf("\n");
    }
}

