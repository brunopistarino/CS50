import random

def main():
    level = get_level()
    current_level = 0
    score = 0

    while current_level < 10:
        x = generate_integer(level)
        y = generate_integer(level)
        tries = 0
        while True:
            try:
                if tries == 3:
                    print(f"{x} + {y} = {x+y}")
                    current_level += 1
                    break
                ans = int(input(f"{x} + {y} = "))
            except:
                print("EEE")
                tries += 1
            else:
                if ans == x + y:
                    current_level += 1
                    score += 1
                    break
                else:
                    print("EEE")
                    tries += 1

    print("Score:", score)


def get_level():
    while True:
        try:
            level = int(input("Level: "))
        except:
            pass
        else:
            if level in [1, 2, 3]:
                return level


def generate_integer(level):
    if level == 1:
        return random.randint(0, pow(10, level))
    else:
        return random.randint(pow(10, level - 1), pow(10, level))


if __name__ == "__main__":
    main()