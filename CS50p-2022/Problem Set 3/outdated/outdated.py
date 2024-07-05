import re

reg1 = "[0-9]+/[0-9]+/[0-9]{4}"
reg2 = "[a-z]+ [0-9]+, [0-9]{4}"

months = [
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december"
]


while True:
    x = input("Date: ").lower().strip()
    try:
        if re.match(reg1, x):
            month, day, year = x.split("/")
        elif re.match(reg2, x):
            x = x.replace(",", "")
            month, day, year = x.split()
            month = months.index(month) + 
        else:
            raise Exception
    except:
        pass
    else:
        month, day = int(month), int(day)
        if month <= 12 and day <= 31:
            break


print(f"{year}-{month:02}-{day:02}")