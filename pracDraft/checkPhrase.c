#include <stdio.h>
#include <cs50.h>
#include <string.h>

void checkPhrase(string a, string b);

int main (void)
{
    string phrase = "blinky";
    string userInput = get_string("please give your guessing password:  ");
    // printf("it is %s", userInput);
    checkPhrase(userInput, phrase);
}


// define checkPhrase function
void checkPhrase(string a, string b)
{
    string x = a;
    string y = b;
    if (strcmp(x,y) == 0)
    {
        printf("Correct guess!");
        printf("\n");
    }
    else
    {
        printf("Wrong guess");
        printf("\n");
    }
}
