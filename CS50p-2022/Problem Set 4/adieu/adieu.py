names = []
while True:
    try:
        name = input("Name: ")
        names.append(name)
    except EOFError:
        print()
        print("Adieu, adieu, to ", end="")
        if len(names) == 1:
            print(names[0])
        elif len(names) == 2:
            print(names[0], "and", names[1])
        else:
            for name in names:
                if name == names[len(names)-1]:
                    print("and", name )
                else:
                    print(name + ", ", end="")
        break