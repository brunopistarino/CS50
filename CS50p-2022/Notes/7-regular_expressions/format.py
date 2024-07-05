import re

name = input("What's your name? ").strip()

if matches := re.search(f"^(.+), *(\w+)$", name):
    name = f"{matches[2]} {matches[1]}"

print(f"hello, {name}")
