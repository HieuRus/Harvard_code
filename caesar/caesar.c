#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

char rotate(char c, int n);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Single argument please \n");
        printf("Usage: ./caesar key \n");
        return 1;
    }

    // check every character in arg[1] is a digit [command line argument]
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (isdigit(argv[1][i]))
        {
            printf("%c is digit", argv[1][i]);
        }
        else
        {
            printf("Usage:  ./caesar key \n");
            return 1;
        }
    }

    // Convert argv[1] from string to an int, user's key
    int key = atoi(argv[1]);
    printf("\n");

    // promp user to input plaintext
    string plainText = get_string("plaintext:  ");

    // call rotate function
    printf("ciphertext: ");
    for (int i = 0; i < strlen(plainText); i++)
    {
        char rotateChar = rotate(plainText[i], key);
        printf("%c", rotateChar);
    }
    printf("\n");
    return 0;
}

// function rotate to shif the character by n key
char rotate(char c, int n)
{
    if (isalpha(c))
    {
        //check upper case character
        if (isupper(c))
        {
            int alphabeticalIndex = (int)c - 65;
            int newAlphaIndex_afterShift = (alphabeticalIndex + n) % 26;
            c = (char)(newAlphaIndex_afterShift + 65); // convert back to ASCII value, and cast to character
        }
        //check lower case character
        if (islower(c))
        {
            int alphabeticalIndex = (int)c - 97;
            int newAlphaIndex_afterShift = (alphabeticalIndex + n) % 26;
            c = (char)(newAlphaIndex_afterShift + 97);
            ;
        }
    }
    return c;
}