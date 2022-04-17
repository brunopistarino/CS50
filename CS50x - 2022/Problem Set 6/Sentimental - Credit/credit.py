from cs50 import get_int

every_other = False
r = 0
digits = 0
input = get_int("Number: ")
n = input

while n > 0:
    digits += 1
    a = n % 10
    n = (n - a) / 10

    if every_other == True:
        x = a * 2
        every_other = False
        if x < 10:
            r += x
        else:
            y = x % 10
            r += y
            r += (x - y) / 10
    else:
        r += a
        every_other = True

if r % 10 == 0:
    if digits == 15 and str(input)[:2] in ["34", "37"]:
        print("AMEX")

    elif digits == 16 and str(input)[:2] in ["51", "52", "53", "54", "55"]:
        print("MASTERCARD")

    elif (digits == 13 and str(input)[:1] == "4") or (digits == 16 and str(input)[:1] == "4"):
        print("VISA")

    else:
        print("INVALID")
else:
    print("INVALID")