#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

typedef uint8_t BYTE;

//bool checkArgcInputProperly(int argc);
bool isExistFile(FILE *file);

int main(int argc, char *argv[])
{
    // allocate the memory for image file, and initialize the variable
    int BLOCK_SIZE = 512;
    BYTE BUFFER[BLOCK_SIZE];
    int imgCounter = 0;
    char filename[8];

    if (argc != 2)
    {
        printf("Usage: ./recover card.raw \n");
        return 1;
    }
    FILE *cardRaw = fopen(argv[1], "r"); // Open memory card
    FILE *Image = NULL;

    if (isExistFile(cardRaw))
    {
        while (fread(BUFFER, 1, BLOCK_SIZE, cardRaw) == BLOCK_SIZE)
        {

            bool isNewJPEG = BUFFER[0] == 0xff && BUFFER[1] == 0xd8 && BUFFER[2] == 0xff && (BUFFER[3] & 0xf0) == 0xe0;
            if (isNewJPEG)
            {
                if (Image != NULL)
                {
                    fclose(Image);
                }

                sprintf(filename, "%03i.jpg", imgCounter++); // make a new JPEG file
                Image = fopen(filename, "w");
                if (Image != NULL)
                {
                    fwrite(BUFFER, sizeof(BYTE), BLOCK_SIZE, Image);
                }
            }
            else
            {
                if (Image != NULL)
                {
                    fwrite(BUFFER, sizeof(BYTE), BLOCK_SIZE, Image);
                }
            }
        }
        fclose(Image);
        fclose(cardRaw);
    }
}

// bool checkArgcInputProperly(int argc)
// {
//     if (argc != 2)
//     {
//         printf("Usage: ./recover card.raw \n");
//         return false;
//     }
//     return true;
// }

// check card raw file existed?
bool isExistFile(FILE *file)
{
    if (file == NULL)
    {
        printf("Could not open a file \n");
        return false;
    }
    return true;
}
