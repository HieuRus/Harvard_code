# TODO
import cs50


def get_moneyOwed():
    while True:
        dollars = cs50.get_float("please input change is owed: ")
        cents = dollars * 100
        if cents > 0:
            return cents
        print("invalid data, please try again")


# calculate the numbers of quaters
def calculate_numberOfQuarters(cents):
    quatersCount = (int(cents / 25))
    return quatersCount


# calculate the numbers of dimes
def calculate_numberOfDimes(cents):
    dimesCount = (int(cents / 10))
    return dimesCount


# calculate the numbers of nickles
def calculate_numberOfNickles(cents):
    nicklesCounts = (int(cents / 5))
    return nicklesCounts


# calculate the numbers of pennies
def calculate_numberOfPennies(cents):
    PenniesCounts = (int(cents / 1))
    return PenniesCounts


# counts TOTAL COINS
def main():
    cents = get_moneyOwed()
    quatersCount = calculate_numberOfQuarters(cents)
    qCents = cents - quatersCount * 25
    dimesCount = calculate_numberOfDimes(qCents)
    dCents = qCents - dimesCount * 10
    nicklesCounts = calculate_numberOfNickles(dCents)
    nCents = dCents - nicklesCounts * 5
    PenniesCounts = calculate_numberOfPennies(nCents)
    pCents = nCents - PenniesCounts * 1
    totalCoints = quatersCount + dimesCount + nicklesCounts + PenniesCounts
    print(f"TOTAL COINS: {totalCoints}")


main()
