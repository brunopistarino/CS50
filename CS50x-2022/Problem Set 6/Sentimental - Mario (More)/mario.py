from cs50 import get_int

while True:
    height = get_int("Height: ")
    if height >= 1 and height <= 8:
        break

for i in range(height):
    for j in range(height):
        if height - (i + 2) < j:
            print("#", end="")
        else:
            print(" ", end="")

    print("  ", end="")

    for j in range(height):
        if not i < j:
            print("#", end="")

    print("")