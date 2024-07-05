from pyfiglet import Figlet
from random import choice
import sys

f = Figlet()
fonts = f.getFonts()

match len(sys.argv):
    case 1:
        font = choice(fonts)
    case 3:
        if sys.argv[1] != "-f" and sys.argv[1] != "--font":
            sys.exit("Invalid usage")
        if not sys.argv[2] in fonts:
           sys.exit("Invalid usage")
        font = sys.argv[2]
    case _:
        sys.exit("Invalid usage")

s = input("Input: ")
f = Figlet(font=font)
print(f.renderText(s))