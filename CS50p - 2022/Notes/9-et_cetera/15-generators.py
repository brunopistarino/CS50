def main():
    n = int(input("What's n? "))
    for s in sheep(n):
        print(s)


def sheep(n):
    for i in range(n):
        # yield provides only one value at a time while the for loop keeps working
        yield "🐑" * i


if __name__ == "__main__":
    main()
