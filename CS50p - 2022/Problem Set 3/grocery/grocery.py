list = {}

while True:
    try:
        x = input().upper()
        list[x] += 1
    except KeyError:
        list[x] = 1
    except EOFError:
        break

for item in sorted(list):
    print(list[item], item)