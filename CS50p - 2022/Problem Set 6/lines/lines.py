import sys

if len(sys.argv) < 2:
    sys.exit("Too few command-line arguments")
if len(sys.argv) > 2:
    sys.exit("Too many command-line arguments")
if sys.argv[1][-3:] != ".py":
    sys.exit("Not a python file")
lines = 0
try:
    with open(sys.argv[1]) as file:
        for line in file:
            line = line.strip()
            if line != "":
                if line[0] != "#":
                    lines += 1
except FileNotFoundError:
    sys.exit("File does not exist")
else:
    print(lines)
