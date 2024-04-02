#include <cs50.h>
#include <stdio.h>

int get_cents(void);
int calculate_quarters(int cents);
int calculate_dimes(int cents);
int calculate_nickels(int cents);
int calculate_pennies(int cents);

int main(void)
{
    // Ask how many cents the customer is owed
    int cents = get_cents();

    // Calculate the number of quarters to give the customer
    int quarters = calculate_quarters(cents);
    cents = cents - quarters * 25;

    // Calculate the number of dimes to give the customer
    int dimes = calculate_dimes(cents);
    cents = cents - dimes * 10;

    // Calculate the number of nickels to give the customer
    int nickels = calculate_nickels(cents);
    cents = cents - nickels * 5;

    // Calculate the number of pennies to give the customer
    int pennies = calculate_pennies(cents);
    cents = cents - pennies * 1;

    // Sum coins
    int coins = quarters + dimes + nickels + pennies;


    // Remove this
    printf("%s %i %s %i %s %i %s %i\n", "quarters:", quarters, " dimes:", dimes, " nickels:", nickels, " pennies:", pennies);

    // Print total number of coins to give the customer
    printf("%i\n", coins);
}


int get_cents(void)
{
    // Promp user to input total cents customer is owed
    int cents;
    do
    {
        cents = get_int("Please enter the total cents customer is owed here:  ");
    }
    while (cents <= 0);
    return cents;
}

int calculate_quarters(int cents)
{
    // Calculate the number of quarters to give to customer
    int quarters = 0;
    for (int i = cents; i >= 25; i = i - 25)
    {
        quarters++;
    }
    return quarters;
}

int calculate_dimes(int cents)
{
    // Calculate the number of dimes to give to customer
    int dimes = 0;
    for (int i = cents; i >= 10; i = i - 10)
    {
        dimes++;
    }
    return dimes;
}

int calculate_nickels(int cents)
{
    // Calculate the number of nickels to give to customer
    int nickels = 0;
    for (int i = cents; i >= 5; i = i - 5)
    {
        nickels++;
    }
    return nickels;
}

int calculate_pennies(int cents)
{
    // Calculate the number of pennies to give to customer
    int pennies = 0;
    for (int i = cents; i >= 1; i = i - 1)
    {
        pennies++;
    }
    return pennies;
}
