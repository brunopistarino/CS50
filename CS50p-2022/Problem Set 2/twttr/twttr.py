str = input("Input: ")
out = ""

for char in str:
    if not char.upper() in ["A", "E", "I", "O", "U"]:
        out += char

print("Output:", out)