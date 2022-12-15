from random import randint

while True:
    try:
        level = int(input("Level: "))
    except:
        pass
    else:
        if level >= 1:
            break

number = randint(1, level)

while True:
    try:
        guess = int(input("Guess: "))
    except:
        pass
    else:
        if guess >= 1:
            if guess < number:
                print("Too small!")
            elif guess > number:
                print("Too large!")
            else:
                print("Just right!")
                break