from cs50 import get_string


def main():
    text = get_string("Text: ")
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_senteces(text)

    L = letters / words * 100
    S = sentences / words * 100

    r = round(0.0588 * L - 0.296 * S - 15.8)

    if r > 16:
        print("Grade 16+")
    elif r < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {r}")


def count_letters(text):
    t = 0
    for char in text:
        if char.isalpha():
            t += 1
    return t


def count_words(text):
    t = 0
    newWord = True
    for char in text:
        if newWord == True and char.isalpha():
            t += 1
            newWord = False
        elif char == " ":
            newWord = True
    return t


def count_senteces(text):
    t = 0
    newSentence = True
    for char in text:
        if newSentence == True and char.isalpha():
            t += 1
            newSentence = False
        elif char in [".", "!", "?"]:
            newSentence = True
    return t


if __name__ == "__main__":
    main()