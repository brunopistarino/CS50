def main():
    yell("This", "is", "CS50")


def yell(*words):
    # map applies the function to each element of a sequence and returns a list
    uppercased = map(str.upper, words)
    print(*uppercased)


if __name__ == "__main__":
    main()
