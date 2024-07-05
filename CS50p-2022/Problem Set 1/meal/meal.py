def main():
    x = input("What time is it? ")
    x = convert(x)

    if 7 <= x <= 8:
        print("breakfast time")
    if 12 <= x <= 13:
        print("lunch time")
    if 18 <= x <= 19:
        print("dinner time")


def convert(time):
    x, y = time.split(":")
    x = int(x)
    y = int(y)
    return x + y / 60


if __name__ == "__main__":
    main()