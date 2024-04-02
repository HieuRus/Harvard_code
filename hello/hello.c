#include <stdio.h>
#include <cs50.h>

int main(void)
{
    printf("Hello, world \n");
    string Name = get_string("What is your Name? \n ");
    printf("Hello %s\n", Name);
}