# TODO
import cs50


# Promp user to input the text
def get_text():
    text = cs50.get_string("please input your text:  ")
    userInput = text.lower()
    return userInput


# Count numbers of letters in the text
def Get_lettersCount(text):
    lettersCount = 0
    for i in range(len(text)):
        if text[i].isalpha() == True:
            lettersCount += 1
    return lettersCount


# Count numbers of words in the text
def get_wordsCount(text):
    Count = 0
    for i in range(len(text)):
        if text[i].isspace() == True:
            Count += 1
        wordsCount = Count + 1
    return wordsCount


# Count numbers of sentences in the text
def get_sentencesCount(text):
    sentencesCount = 0
    for i in range(len(text)):
        if text[i] == ".":
            sentencesCount += 1
        if text[i] == "!":
            sentencesCount += 1
        if text[i] == "?":
            sentencesCount += 1
    return sentencesCount


# Calculation grade based on Coleman-Liau's formula
def calculation_gradeLevel(lettersCount, wordsCount, sentencesCount):
    L = (lettersCount / wordsCount) * 100
    S = (sentencesCount / wordsCount) * 100
    Grade = 0.0588 * L - 0.296 * S - 15.8
    grade = round(Grade)
    return grade


# define main
def main():
    userInput = get_text()
    lettersCount = Get_lettersCount(userInput)
    wordsCount = get_wordsCount(userInput)
    sentencesCount = get_sentencesCount(userInput)
    gradeLevel = calculation_gradeLevel(lettersCount, wordsCount, sentencesCount)
    if gradeLevel >= 16:
        print("Grade 16+")
    elif gradeLevel < 1:
        print("Before Grade 1")
    else:
        print(f"Grade: {gradeLevel}")


# call main
main()
