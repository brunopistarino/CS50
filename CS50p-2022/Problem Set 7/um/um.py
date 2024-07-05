import re
import sys


def main():
    print(count(input("Text: ")))


def count(s):
    return len(re.findall(r"(\Wum\W|^um\W|\Wum$|^um$)", s, re.IGNORECASE))


if __name__ == "__main__":
    main()