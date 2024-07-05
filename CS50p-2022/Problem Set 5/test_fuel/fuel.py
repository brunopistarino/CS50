def main():
    while True:
        try:
            fraction = input("Fraction: ")
            percentage = convert(fraction)
            print(gauge(percentage))
        except:
            pass
        else:
            break


def convert(fraction):
    x, y = fraction.split("/")
    x, y = int(x), int(y)
    return round(x / y * 100)


def gauge(percentage):
    if percentage <= 1:
        return "E"
    if percentage >= 99:
        return "F"
    return f"{percentage}%"


if __name__ == "__main__":
    main()
