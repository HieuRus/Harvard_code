#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Promp user to give the text
    string userText = get_string("text here - not digit:  ");
    //check to make sure user's input text does not have digit
    for (int j = 0; j < strlen(userText); j++)
    {
        if (isdigit(userText[j]))
        {
            userText = get_string("text, not digit please:  ");
        }
    }
    int lettersCount = count_letters(userText);
    int wordsCount = count_words(userText);
    int sentencesCount = count_sentences(userText);

    // Calculate Grade
    double L = ((double)lettersCount / (double)wordsCount) * 100;  // the average number if letters per 100 words
    double S = ((double)sentencesCount / (double)wordsCount) * 100; //the average number of sentences per 100 words
    double X = 0.0588 * L - 0.296 * S - 15.8;
    int Grade = round(X);
    if (Grade < 1)
    {
        printf("Before Grade 1");
    }
    else if (Grade >= 1 && Grade < 16)
    {
        printf("Grade %i", Grade);
    }
    else
    {
        printf("Grade 16+");
    }
    printf("\n");

}

// Count total letters of the text given from users
int totalLetters = 0;
int count_letters(string text)
{
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            totalLetters += 1;
        }
    }
    return totalLetters;
}

// Count total words of the text given from users
int totalWords;
int count_words(string text)
{
    int totalSpaceCount = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isspace(text[i]))
        {
            totalSpaceCount += 1;
        }
    }
    totalWords = totalSpaceCount + 1;
    return totalWords;
}

// Count total sentences of the text given from users
int totalSentences = 0;
int count_sentences(string text)
{
    for (int i = 0; i < strlen(text); i++)
    {
        if ((int)(text[i]) == 46)
        {
            totalSentences += 1;
        }

        if ((int)(text[i]) == 33)
        {
            totalSentences += 1;
        }

        if ((int)(text[i]) == 63)
        {
            totalSentences += 1;
        }
    }
    return totalSentences;
}