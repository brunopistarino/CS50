import re
import sys


def main():
    print(validate(input("IPv4 Address: ")))


def validate(ip):
    regex = r"(\d){1,3}\.(\d){1,3}\.(\d){1,3}\.(\d){1,3}"
    if match := re.match(regex, ip):
        n1, n2, n3, n4 = match.group().split(".")
        n1, n2, n3, n4 = int(n1), int(n2), int(n3), int(n4)
        return n1 <= 255 and n2 <= 255 and n3 <= 255 and n4 <= 255
    return False


...


if __name__ == "__main__":
    main()