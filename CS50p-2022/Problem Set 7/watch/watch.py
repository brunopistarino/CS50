import re
import sys


def main():
    print(parse(input("HTML: ")))


def parse(s):
    regex = r'youtube\.com/embed/(\w+)"'
    if match := re.search(regex, s):
        return "https://youtu.be/" + match.group(1)


if __name__ == "__main__":
    main()