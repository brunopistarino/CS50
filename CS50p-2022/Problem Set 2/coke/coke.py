x = 0
while True:
    n = int(input("Insert coin: "))

    if n in [5, 10, 25, 50]:
        x += n

    if x < 50:
        print("Amount due: ", 50 - x)
    else:
        break

print("Change owed: ", x - 50)