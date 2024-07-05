import re
import sys


def main():
    print(convert(input("Hours: ")))


def convert(s):
    regex = r"^(0?[0-9]|1[0-2])(?::([0-5][0-9]))? (AM|PM) to (0?[0-9]|1[0-2])(?::([0-5][0-9]))? (AM|PM)$"
    if match := re.match(regex, s):
        h1 = int(match.group(1))
        m1 = match.group(2) or 0
        t1 = match.group(3)
        h2 = int(match.group(4))
        m2 = match.group(5) or 0
        t2 = match.group(6)

        if t1 == "PM":
            if h1 < 12:
                h1 += + 12
        elif h1 == 12:
            h1 = 0

        if t2 == "PM":
            if h2 < 12:
                h2 += 12
        elif h1 == 12:
            h1 = 0

        return f"{h1:02}:{m1:02} to {h2:02}:{m2:02}"
    raise(ValueError)

if __name__ == "__main__":
    main()