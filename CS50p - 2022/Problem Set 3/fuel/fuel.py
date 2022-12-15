while True:
    fraction = input("Fraction: ")
    try:
        x, y = fraction.split("/")
        x, y = int(x), int(y)
        r = round(x / y * 100)
    except ValueError:
        pass
    except ZeroDivisionError:
        pass
    else:
        if x <= y:
            if r <= 1:
                print("E")
            elif r >= 99:
                print("F")
            else:
                print(f"{r}%")
            break