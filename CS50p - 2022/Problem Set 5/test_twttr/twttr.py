def main():
    word = input("Input: ")
    print("Output:", shorten(word))


def shorten(word):
    out = ""
    for char in word:
        if not char.upper() in ["A", "E", "I", "O", "U"]:
            out += char
    return out


if __name__ == "__main__":
    main()
