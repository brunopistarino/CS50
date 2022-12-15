import sys
from PIL import Image, ImageOps

if len(sys.argv) < 3:
    sys.exit("Too few command-line arguments")
if len(sys.argv) > 3:
    sys.exit("Too many command-line arguments")
if not sys.argv[1].split(".")[-1] in ["jpg", "jpeg", "png"]:
    sys.exit("Invalid input")
if not sys.argv[2].split(".")[-1] in ["jpg", "jpeg", "png"]:
    sys.exit("Invalid output")
if sys.argv[1].split(".")[-1] != sys.argv[2].split(".")[-1]:
    sys.exit("Input and output have different extensions")

img = Image.open(sys.argv[1])
shirt = Image.open("shirt.png")

out = ImageOps.fit(img, shirt.size)
out.paste(shirt, shirt)

img.close()
shirt.close()

out.save(sys.argv[2])