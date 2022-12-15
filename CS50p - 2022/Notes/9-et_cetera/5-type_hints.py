def meow(n: int) -> str:
    return "meow\n" * n


number: int = int(input("Number: "))
meows: str = meow(number)
print(meows, end="")

# run type error checking with:
# python -m mypy 4-type_hints.py
# or
# mypy 4-type_hints.py
