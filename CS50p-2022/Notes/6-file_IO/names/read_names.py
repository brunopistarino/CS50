names = []

# "r" is the default mode, so it's not necessary to specify it
with open("names.txt") as file:
    for line in file:
        names.append(line.strip())

for name in names:
    print(f"hello {name}")
