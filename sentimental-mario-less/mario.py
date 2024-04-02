# TODO
import cs50


# promp the user to get pyramid's height
def get_Height():
    while True:
        height = cs50.get_int("Height of pyramid: ")
        if height >= 1 and height <= 8:
            return height
        print("Height should be between 1-8, please try again")


# print the half-pyramid based on user's input for the height
def main():
    height = get_Height()
    for i in range(0, height):
        print(" " * (height - i - 1), end="")
        print("#" * (i + 1))
    i += 1


print()


main()