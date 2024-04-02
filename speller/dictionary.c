// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <strings.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;
int totalWordsInDictionary = 0;
int maxHashCode = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int hashCode = hash(word);

    for (node *cursor = table[hashCode]; cursor != NULL; cursor = cursor->next)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int hash = 601;
    int c;

    while (*word != '\0')
    {
        hash = ((hash << 4) + (int)(tolower(*word))) % LENGTH;
        word++;
    }

    return hash % LENGTH;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    int wordCount = 0;
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        printf("could not open the dictionary file");
        return false;
    }
    else
    {
        char BUFFER[LENGTH + 1];
        while (fscanf(dict, "%s", BUFFER) != EOF) // read from dictionary to buffer
        {
            node *n = malloc(sizeof(node)); // using malloc to ask for memory enough to store a word
            if (n == NULL)
            {
                return false;
            }
            else
            {
                strcpy(n->word, BUFFER);
                int hashCode = hash(n->word); // run has function on the word to find the hash code [index in the hash table]
                n->next = table[hashCode];    // insert new node to hash table
                table[hashCode] = n;
                wordCount++;

                if (hashCode > maxHashCode)
                {
                    maxHashCode = hashCode;
                }
            }
        }
    }
    totalWordsInDictionary = wordCount;
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return (totalWordsInDictionary);
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO

    for (int i = 0; i <= maxHashCode; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}
