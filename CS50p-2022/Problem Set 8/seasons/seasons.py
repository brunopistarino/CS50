from datetime import date
import re, sys, inflect

def main():
    date = get_date(input("Date of Birth: "))

    if not date:
        sys.exit("Invalid date")

    minutes = get_minutes(date)
    print(minutes_to_words(minutes).capitalize())


def get_date(s):
    regex = r"\d{4}-\d{2}-\d{2}"
    if match := re.match(regex, s):
        year, month, day = map(int, match.group().split("-"))
        return date(year, month, day)
    return False


def get_minutes(date):
    now = date.today()
    return (now - date).days * 24 * 60


def minutes_to_words(minutes):
    p = inflect.engine()
    return p.number_to_words(minutes, andword="") + " minutes"


if __name__ == "__main__":
    main()

# 2000-10-10